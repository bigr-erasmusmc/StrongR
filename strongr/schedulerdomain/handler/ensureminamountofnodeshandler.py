import strongr.core
import logging

class EnsureMinAmountOfNodesHandler(object):
    def __call__(self, command):
        config = strongr.core.Core.config()
        templates = config.schedulerdomain.simplescaler.templates.as_dict()
        logger = logging.getLogger(self.__class__.__name__)

        cloudQueryBus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getCloudServiceByName(config.clouddomain.driver).getQueryBus()
        cloudQueryFactory = strongr.core.domain.clouddomain.CloudDomain.queryFactory()

        machines = cloudQueryBus.handle(cloudQueryFactory.newListDeployedVms())

        template_counters = {}
        machines_needed = {}
        for machine in machines:
            for template_name in templates:
                if machine.startswith(template_name + '-'):
                    if template_name in template_counters:
                        template_counters[template_name] += 1
                    else:
                        template_counters[template_name] = 1
                    break

        for template_name in templates:
            if template_name in template_counters and template_counters[template_name] < templates[template_name]['spawned-min']:
                machines_needed[template_name] = templates[template_name]['spawned-min'] - template_counters[template_name]
            else:
                machines_needed[template_name] = templates[template_name]['spawned-min']


        if len(machines_needed) > 0:
            logger.info('Machines needed: {}'.format(machines_needed))
        else:
            logger.info('No aditional machines needed!')
