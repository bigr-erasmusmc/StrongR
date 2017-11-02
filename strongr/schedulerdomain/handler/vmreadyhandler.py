import strongr.core.gateways
from strongr.schedulerdomain.model import Vm, VmState

class VmReadyHandler(object):
    def __call__(self, command):
        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        try:
            session.query(Vm).filter(Vm.vm_id == command.vm_id).update({Vm.state: VmState.READY}, synchronize_session='evaluate')
            session.commit()
        except:
            session.rollback()
            raise
