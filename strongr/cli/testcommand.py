from sqlalchemy import func, and_, or_

from strongr.schedulerdomain.model import Job, JobState, VmState, Vm
from .wrapper import Command

import strongr.core.gateways

class TestCommand(Command):
    """
    Runs experimental testcode

    test:run
    """
    def handle(self):
        #command_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getCommandBus()
        #command_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.commandFactory()

        #command_bus.handle(command_factory.newScaleIn())

        # check for VM's marked for death without jobs

        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        subquery = session.query(Job.vm_id,
                                 func.count(Job.job_id).label('jobs')) \
            .filter(
            Job.state.in_([JobState.ASSIGNED, JobState.RUNNING])
        ).group_by(Job.vm_id).subquery('j')
        marked_for_death_vms = session.query(Vm) \
            .outerjoin(subquery, subquery.c.vm_id == Vm.vm_id) \
            .filter(and_(Vm.state == VmState.MARKED_FOR_DEATH, or_(subquery.c.jobs is None, subquery.c.jobs == 0))) \
            .all()

        from pprint import pprint
        pprint(marked_for_death_vms)
