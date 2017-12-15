import strongr.core

import strongr.core.domain.schedulerdomain
import strongr.core.domain.clouddomain
import strongr.core.gateways

from sqlalchemy import and_
from datetime import datetime, timedelta

from strongr.schedulerdomain.model import Job, JobState


class CheckJobsRunningHandler:
    def __call__(self, command):
        session = strongr.core.gateways.Gateways.sqlalchemy_session()

        deadline = datetime.utcnow() - timedelta(minutes=15)

        for job in session.query(Job).filter(and_(Job.state == JobState.RUNNING, Job.state_date < deadline)).all():
            cloudQueryBus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getQueryBus()
            cloudQueryFactory = strongr.core.domain.clouddomain.CloudDomain.queryFactory()

            status = cloudQueryBus.handle(cloudQueryFactory.newRequestJidStatus(job.job_id))

            from pprint import pprint
            pprint(status)

            if status is None:
                # job not finished yet
                continue

        exit(0)

        session.query().filter(Job.job_id==command.job_id).update({Job.state: JobState.FINISHED})
        session.commit()
