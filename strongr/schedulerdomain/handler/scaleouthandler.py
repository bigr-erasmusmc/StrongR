import uuid

import strongr.core
import strongr.core.gateway
import logging

class ScaleOutHandler(object):
    def __call__(self, command):
        config = strongr.core.Core.config()
        cache = strongr.core.gateway.Gateway.cache()
        logger = logging.getLogger('schedulerdomain.' + self.__class__.__name__)

        templates = config.schedulerdomain.simplescaler.templates.as_dict()

        if cache.exists('scaleout'):
            scaleout = cache.get('scaleout')
            command.cores -= scaleout['cores']
            command.ram -= scaleout['ram']

        if command.cores <= 0 or command.cores < config.schedulerdomain.simplescaler.scaleoutmincoresneeded:
            return

        if command.ram <= 0 or command.ram < config.schedulerdomain.simplescaler.scaleoutminramneeded:
            return

        for template in templates:
            templates[template]['ram_per_core'] = templates[template]['ram'] / templates[template]['cores']

        ram_per_core_needed = command.ram / command.cores

        # find best fit based on templates
        template = min(templates, key=lambda key: abs(templates[key]['ram_per_core'] - ram_per_core_needed))

        # scaleout by one instance

        if not cache.exists('scaleout'):
            scaleout = {'cores': 0, 'ram': 0}
        else:
            # make sure we have the most recent version of scaleout
            scaleout = cache.get('scaleout')
        scaleout['cores'] += templates[template]['cores']
        scaleout['ram'] += templates[template]['ram']
        cache.set('scaleout', scaleout, 3600)

        cloudServices = strongr.core.domain.clouddomain.CloudDomain.cloudService()
        cloudCommandFactory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()
        cloudProviderName = config.clouddomain.driver
        profile = getattr(config.clouddomain, cloudProviderName).default_profile if 'profile' not in templates[template] else templates[template]['profile']
        deployVmsCommand = cloudCommandFactory.newDeployVmsCommand(names=[template + '-' + str(uuid.uuid4())], profile=profile, cores=templates[template]['cores'], ram=templates[template]['ram'])

        cloudService = cloudServices.getCloudServiceByName(cloudProviderName)
        cloudCommandBus = cloudService.getCommandBus()

        logger.info('Deploying VM {0} cores={1} ram={2}GiB'.format(deployVmsCommand.names[0], deployVmsCommand.cores, deployVmsCommand.ram))

        cloudCommandBus.handle(deployVmsCommand)
