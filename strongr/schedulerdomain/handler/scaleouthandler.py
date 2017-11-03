import uuid

import strongr.core
import strongr.core.gateways
import logging

class ScaleOutHandler(object):
    def __call__(self, command):
        return # turn off for testing purposes

        if strongr.core.gateways.Gateways.lock('scaleout-lock').exists():
            return # only every run one of these commands at once

        with strongr.core.gateways.Gateways.lock('scaleout-lock'):  # only ever run one of these commands at once
            config = strongr.core.Core.config()
            cache = strongr.core.gateways.Gateways.cache()
            logger = logging.getLogger('schedulerdomain.' + self.__class__.__name__)

            templates = dict(config.schedulerdomain.simplescaler.templates.as_dict()) # make a copy because we want to manipulate the list

            if cache.exists('scaleout'):
                scaleout = cache.get('scaleout')
                command.cores -= scaleout['cores']
                command.ram -= scaleout['ram']
                for template in list(templates):
                    if template in scaleout['spawned'] and templates[template]['spawned-max'] <= scaleout['spawned'][template]:
                        del(templates[template]) # we already have the max amount of vms for this template

            if not templates:
                return # max env size reached or no templates defined in config

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
                scaleout = {'cores': 0, 'ram': 0, 'spawned': {template: 0}}
            else:
                # make sure we have the most recent version of scaleout
                scaleout = cache.get('scaleout')
                if template not in scaleout['spawned']:
                    scaleout['spawned'][template] = 0
            scaleout['cores'] += templates[template]['cores']
            scaleout['ram'] += templates[template]['ram']
            scaleout['spawned'][template] += 1
            cache.set('scaleout', scaleout, 3600)

            cloudService = strongr.core.domain.clouddomain.CloudDomain.cloudService()
            cloudCommandFactory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()
            cloudProviderName = config.clouddomain.driver
            profile = getattr(config.clouddomain, cloudProviderName).default_profile if 'profile' not in templates[template] else templates[template]['profile']
            deployVmsCommand = cloudCommandFactory.newDeployVmsCommand(names=[template + '-' + str(uuid.uuid4())], profile=profile, cores=templates[template]['cores'], ram=templates[template]['ram'])

            cloudCommandBus = cloudService.getCommandBus()

            logger.info('Deploying VM {0} cores={1} ram={2}GiB'.format(deployVmsCommand.names[0], deployVmsCommand.cores, deployVmsCommand.ram))

            cloudCommandBus.handle(deployVmsCommand)
