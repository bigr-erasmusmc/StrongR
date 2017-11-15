import strongr.core.domain.clouddomain
from sqlalchemy import and_, func
from strongr.schedulerdomain.model import Vm, VmState
from datetime import datetime, timedelta

import logging

class CleanupNodesHandler(object):
    def __call__(self, command):
        cloud_command_factory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()
        cloud_command_bus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getCommandBus()


        deadline = datetime.now() - timedelta(hours=3) # give cloud domain 3 hours to provision a machine, if it isn't online by then it will probably never be
        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        result = session.query(Vm).filter(and_(Vm.state.in_([VmState.NEW, VmState.PROVISION]), Vm.state_date < deadline)).all()

        for vm in result:
            try:
                command = cloud_command_factory.newDestroyVmsCommand([vm.vm_id])
                cloud_command_bus.handle(command)
            except Exception as e:
                # sometimes VM doesn't exist in salt-cloud triggering this exception
                logging.getLogger("CleanupNodesHandler").warning(e)
