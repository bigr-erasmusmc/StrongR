# from sqlalchemy import func, and_, or_
#
# from strongr.schedulerdomain.model import Job, JobState, VmState, Vm
from .wrapper import Command
#
# import strongr.core.gateways

import strongr.core.domain.schedulerdomain

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
        #from pprint import pprint
        #session = strongr.core.gateways.Gateways.sqlalchemy_session()
        # check for VM's marked for death without jobs
        #subquery = session.query(Job.vm_id,
        #                          func.count(Job.job_id).label('jobs')) \
        #     .filter(
        #     Job.state.in_([JobState.ASSIGNED, JobState.RUNNING])
        # ).group_by(Job.vm_id).subquery('j')
        # marked_for_death_vms = session.query(Vm) \
        #     .outerjoin(subquery, subquery.c.vm_id == Vm.vm_id) \
        #     .filter(and_(Vm.state == VmState.MARKED_FOR_DEATH, or_(subquery.c.jobs == None, subquery.c.jobs == 0))) \
        #     .all()
        #
        # pprint(marked_for_death_vms)

        command_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.commandFactory()
        command_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getCommandBus()

        command_bus.handle(command_factory.newCheckJobsRunning())
