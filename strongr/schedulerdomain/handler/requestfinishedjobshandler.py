import strongr.core.gateways
from strongr.schedulerdomain.model import Job, JobState

class RequestFinishedJobsHandler(object):
    def __call__(self, query, *args, **kwargs):
        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        result = session.query(Job).filter(Job.state.in_([JobState.FAILED, JobState.FINISHED])).order_by(
            Job.job_id).all()

        job_ids = []
        for job in result:
            job_ids.append(job.job_id)
        return job_ids
