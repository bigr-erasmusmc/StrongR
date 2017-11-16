import strongr.core.domain.clouddomain
from sqlalchemy import and_, func
from strongr.schedulerdomain.model import Vm, VmState
from datetime import datetime, timedelta

import strongr.core

class CleanupNodesHandler(object):
    def __call__(self, command):
        cloud_command_factory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()
        cloud_command_bus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getCommandBus()
        cloud_query_factory = strongr.core.domain.clouddomain.CloudDomain.queryFactory()
        cloud_query_bus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getQueryBus()

        vm_templates = strongr.core.Core.config().schedulerdomain.simplescaler.templates.as_dict()

        deadline = datetime.now() - timedelta(hours=3) # give cloud domain 3 hours to provision a machine, if it isn't online by then it will probably never be
        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        vms_in_db = session.query(Vm).filter(and_(Vm.state.in_([VmState.NEW, VmState.PROVISION]), Vm.state_date < deadline)).all()

        vms_in_cloud = cloud_query_bus.handle(cloud_query_factory.newListDeployedVms())

        parallel_remove_list = []
        for vm in vms_in_db:
            if vm in vms_in_cloud['up'] or vm in vms_in_cloud['down']:
                parallel_remove_list.append(vm)
            else: # vm was never up or manually destroyed
                vm.state = VmState.DESTROYED
                session.commit()


        # cleanup unsynced / unregistered VM's
        for template in vm_templates:
            for vm in vms_in_cloud['up']:
                if vm not in vms_in_db and vm.startswith(template + '-'):
                    parallel_remove_list.append(vm)

            for vm in vms_in_cloud['down']:
                if  vm not in vms_in_db and vm.startswith(template + '-'):
                    parallel_remove_list.append(vm)


        if len(parallel_remove_list) > 0:
            command = cloud_command_factory.newDestroyVmsCommand(parallel_remove_list)
            cloud_command_bus.handle(command)
