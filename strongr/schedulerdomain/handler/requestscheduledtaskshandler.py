import strongr.core.gateways
from strongr.schedulerdomain.model import Job, JobState

class RequestScheduledTasksHandler:
    def __call__(self, query):
        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        result = session.query(Job).filter_by(Job.state.notin_([JobState.FAILED, JobState.FINISHED])).order_by(Job.job_id).all()
        return result
