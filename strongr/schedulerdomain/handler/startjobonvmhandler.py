import strongr
import strongr.core.domain.schedulerdomain
import strongr.core.domain.clouddomain
from strongr.core.gateways import Gateways
from strongr.schedulerdomain.model import Job


class StartJobOnVmHandler:
    def __call__(self, command):
        db = strongr.core.gateways.Gateways.sqlalchemy_session()
        try:
            db.query().filter(Job.job_id == command.job_id).update({Job.vm_id: command.vm_id}, synchronize_session=False)
            db.commit()
        except:
            db.rollback()
            raise
