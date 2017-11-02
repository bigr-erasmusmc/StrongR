import strongr.core.gateways

from strongr.schedulerdomain.model import Job, JobState

class JobFinishedHandler(object):
    def __init__(self, command):
        db = strongr.core.gateways.Gateways.sqlalchemy_session()
        try:
            jobstate = (JobState.FINISHED if command.retcode == 0 else JobState.FAILED)
            db.query(Job).filter(Job.job_id == command.job_id).update(
                {
                    Job.state: jobstate,
                    Job.stdout: command.ret,
                    Job.return_code: command.retcode
                },
                synchronize_session='evaluate'
            )
            from pprint import pprint
            pprint(command)
            db.commit()
        except:
            db.rollback()
            raise
