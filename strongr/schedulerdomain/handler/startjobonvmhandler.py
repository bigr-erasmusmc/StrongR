import strongr
import strongr.core.domain.schedulerdomain
import strongr.core.domain.clouddomain
from strongr.core.gateways import Gateways
from strongr.schedulerdomain.model import Job, JobState


class StartJobOnVmHandler:
    def __call__(self, command):
        db = strongr.core.gateways.Gateways.sqlalchemy_session()
        try:
            db.query(Job).filter(Job.job_id == command.job_id).update({Job.vm_id: command.vm_id, Job.state: JobState.RUNNING}, synchronize_session='evaluate')
            db.commit()
        except:
            db.rollback()
            raise
