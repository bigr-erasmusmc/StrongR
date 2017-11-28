import strongr.core.gateways
import strongr.core
from strongr.schedulerdomain.model import Vm, VmState

from datetime import datetime, timedelta

class VmReadyHandler(object):
    def __call__(self, command):
        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        try:
            template = command.vm_id.split('-')[0]
            if len(template) > 0:
                templates = strongr.core.Core.config().schedulerdomain.simplescaler.templates.as_dict()
                for t in templates:
                    if t == template:
                        deadline = datetime.utcnow() + timedelta(seconds=(templates[t]['maxage'] if hasattr(templates[t], 'maxage') else 900))
            else:
                deadline = datetime.utcnow() + timedelta(minutes=15)

            session.query(Vm).filter(Vm.vm_id == command.vm_id).update({Vm.state: VmState.READY, Vm.deadline: deadline}, synchronize_session='evaluate')
            session.commit()
        except:
            session.rollback()
            raise
