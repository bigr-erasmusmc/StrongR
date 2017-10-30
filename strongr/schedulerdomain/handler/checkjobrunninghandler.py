import strongr.core
import os

import strongr.core.domain.schedulerdomain
import strongr.core.domain.clouddomain
import strongr.core.gateways

from strongr.schedulerdomain.model import Job, JobState


class CheckJobRunningHandler:
    def __call__(self, command):
        core = strongr.core.getCore()

        cloudQueryBus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getCloudServiceByName(core.config().clouddomain.driver).getQueryBus()
        cloudQueryFactory = strongr.core.domain.clouddomain.CloudDomain.queryFactory()

        status = cloudQueryBus.handle(cloudQueryFactory.newRequestJidStatus(command.job_id))
        if status == None and not status:
            # job not finished yet
            return

        os.remove('/tmp/strongr/' + command.job_id)

        db = strongr.core.gateways.Gateways.sqlalchemy_session()
        db.query().filter(Job.job_id==command.job_id).update({Job.state: JobState.FINISHED})
        db.commit()
