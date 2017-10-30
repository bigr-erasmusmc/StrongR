import strongr.core.gateways
from strongr.schedulerdomain.model import Job, JobState


class ScheduleJobHandler:
    def __call__(self, command):
        job = Job()
        job.job_id = command.job_id
        job.state = JobState.ENQUEUED
        job.cores = command.cores
        job.ram = command.ram
        job.cmd = command.cmd
        job.vm = None

        session = strongr.core.gateways.Gateways.sqlalchemy_session()
        session.add(job)
        session.commit()
