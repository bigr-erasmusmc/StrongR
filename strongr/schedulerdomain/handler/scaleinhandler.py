import strongr.core
import strongr.core.gateways

import logging

from sqlalchemy import func, and_, or_

from strongr.schedulerdomain.model import JobState, Job, Vm, VmState


class ScaleOutHandler(object):
    def __call__(self, command):
        if strongr.core.gateways.Gateways.lock('scaleout-lock').exists():
            return # only every run one of these commands at once

        with strongr.core.gateways.Gateways.lock('scaleout-lock'):  # only ever run one of these commands at once
            logger = logging.getLogger('schedulerdomain.' + self.__class__.__name__)

            session = strongr.core.gateways.Gateways.sqlalchemy_session()

            # subquery to see whats already running on vm
            subquery = session.query(Job.vm_id, func.sum(Job.cores).label('cores'), func.sum(Job.ram).label('ram')).filter(
                Job.state.in_([JobState.RUNNING])).group_by(Job.vm_id).subquery('j')

            query = session.query(Vm.vm_id) \
                .outerjoin(subquery, subquery.c.vm_id == Vm.vm_id) \
                .filter(
                and_(
                    or_(
                        and_(  # case 1 - vm with jobs, check if vm has about half capacity available
                            Vm.cores - subquery.c.cores >= Vm.cores / 2,
                            Vm.ram - subquery.c.ram >= Vm.ram / 2
                        ),
                        and_(  # case 2 - vm with no jobs
                            subquery.c.cores == None,
                            subquery.c.ram == None,
                        )
                    ),
                    Vm.state.in_([VmState.READY])  # vm should be in state ready
                )
            )

            results = query.all()

            if not results:
                return # no VM's to scalein



