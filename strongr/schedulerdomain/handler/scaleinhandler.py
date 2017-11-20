import strongr.core
import strongr.core.gateways

import logging

from sqlalchemy import func, and_, or_

from strongr.schedulerdomain.model import JobState, Job, Vm, VmState

from datetime import datetime, timedelta

class ScaleInHandler(object):
    def __call__(self, command):
        if strongr.core.gateways.Gateways.lock('scaleout-lock').exists():
            return # only every run one of these commands at once

        with strongr.core.gateways.Gateways.lock('scaleout-lock'):  # only ever run one of these commands at once
            logger = logging.getLogger('schedulerdomain.' + self.__class__.__name__)

            session = strongr.core.gateways.Gateways.sqlalchemy_session()

            # subquery to see whats already running on vm
            subquery1 = session.query(Job.vm_id, func.count(Job.job_id).label('jobs'), func.sum(Job.cores).label('cores'), func.sum(Job.ram).label('ram')).filter(
                Job.state.in_([JobState.RUNNING])).group_by(Job.vm_id).subquery('j')

            subquery2 = session.query(Job.vm_id, func.max(Job.state_date).label('last_job_date')).filter(Job.state.in_([JobState.FAILED, JobState.FINISHED, JobState.RUNNING])).group_by(Job.vm_id).subquery('i')

            results = session.query(Vm.vm_id.label('vm_id'), subquery1.c.jobs.label('job_count'), subquery2.c.last_job_date) \
                .outerjoin(subquery1, subquery1.c.vm_id == Vm.vm_id) \
                .outerjoin(subquery2, subquery2.c.vm_id == Vm.vm_id) \
                .filter(
                and_(
                    or_(
                        and_(  # case 1 - vm with jobs, check if vm has about half capacity available
                            Vm.cores - subquery1.c.cores >= Vm.cores / 2,
                            Vm.ram - subquery1.c.ram >= Vm.ram / 2
                        ),
                        and_(  # case 2 - vm with no jobs
                            subquery1.c.cores == None,
                            subquery1.c.ram == None,
                        )
                    ),
                    Vm.state.in_([VmState.READY])  # vm should be in state ready
                )
            ).all()

            if not results:
                return # no VM's to scalein

            deadline = datetime.now() + timedelta(minutes=-10)

            vms_to_update = []
            mark_for_death_counter = 0
            for vm in results:
                if vm[1] is None or vm[1] == 0:
                    vms_to_update.append(vm[0])
                elif deadline > vm[2]:
                    if mark_for_death_counter % 2 == 0:
                        vms_to_update.append(vm)
                    mark_for_death_counter += 1

            if len(vms_to_update) > 0:
                try:
                    session.commit()
                    session.query(Vm).filter(Vm.vm_id.in_(vms_to_update)).update({Vm.state: VmState.MARKED_FOR_DEATH}, synchronize_session='fetch')
                    session.commit()
                except Exception as e:
                    session.rollback()
                    logger.warning(e)
