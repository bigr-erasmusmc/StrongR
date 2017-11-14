import strongr.core.domain.clouddomain
from sqlalchemy import and_, func
from strongr.schedulerdomain.model import Vm, VmState
from datetime import datetime, timedelta

class CleanupNodesHandler(object):
    def __call__(self, command):
        cloud_command_factory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()
        cloud_command_handler = strongr.core.domain.clouddomain.CloudDomain.cloudService()


        since = datetime.now() - timedelta(hours=3)
        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        result = session.query(Vm).filter(and_(Vm.state.in_([VmState.NEW, VmState.PROVISION]), Vm.state_date > since)).all()

        vm_ids = []
        for vm in result:
            vm_ids.append(vm.vm_id)

        session.delete(result)
        session.commit()

        command = cloud_command_factory.newDestroyVms(vm_ids)
        cloud_command_handler.handle(command)
