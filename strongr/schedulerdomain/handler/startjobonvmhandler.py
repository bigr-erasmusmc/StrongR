import strongr
import strongr.core.domain.clouddomain
from strongr.core.gateways import Gateways
from strongr.schedulerdomain.model import Job, JobState


class StartJobOnVmHandler:
    def __call__(self, command):
        db = strongr.core.gateways.Gateways.sqlalchemy_session()
        try:
            db.query(Job).filter(Job.job_id == command.job_id).update({Job.vm_id: command.vm_id, Job.state: JobState.RUNNING}, synchronize_session='evaluate')
            db.commit()

            job = db.query(Job).filter(Job.job_id == command.job_id).all()[0]

            cloudCommandBus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getCommandBus()
            cloudCommandFactory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()

            cloudCommandBus.handle(cloudCommandFactory.newRunShellCodeCommand(job_id=job.job_id, sh=job.cmd, host=job.vm_id))
        except:
            db.rollback()
            raise


