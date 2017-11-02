import strongr.core.gateways

from strongr.schedulerdomain.model import Job, JobState

class JobFinishedHandler(object):
    def __init__(self, command):
        db = strongr.core.gateways.Gateways.sqlalchemy_session()
        try:
            db.query(Job).filter(Job.job_id == command.job_id).update(
                {
                    Job.state: (JobState.FINISHED if command.retcode == 0 else JobState.FAILED),
                    Job.stdout: command.ret,
                    Job.return_code: command.retcode
                },
                synchronize_session='evaluate'
            )
            db.commit()
        except:
            db.rollback()
            raise
