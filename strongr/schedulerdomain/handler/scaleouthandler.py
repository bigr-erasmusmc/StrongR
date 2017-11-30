import uuid

import strongr.core
import strongr.core.gateways
import logging
import strongr.core.domain.schedulerdomain
from strongr.schedulerdomain.model import VmState


class ScaleOutHandler(object):
    def __call__(self, command):
        if strongr.core.gateways.Gateways.lock('scaleout-lock').exists():
            return # only every run one of these commands at once

        with strongr.core.gateways.Gateways.lock('scaleout-lock'):  # only ever run one of these commands at once
            config = strongr.core.Core.config()
            logger = logging.getLogger('schedulerdomain.' + self.__class__.__name__)

            query_factory = strongr.core.domain.schedulerdomain.SchedulerDomain.queryFactory()
            query_bus = strongr.core.domain.schedulerdomain.SchedulerDomain.schedulerService().getQueryBus()

            templates = dict(config.schedulerdomain.simplescaler.templates.as_dict()) # make a copy because we want to manipulate the list

            active_vms = query_bus.handle(query_factory.newRequestVms([VmState.NEW, VmState.PROVISION, VmState.READY]))

            provision_counter = 0
            for vm in active_vms:
                if vm.state in [VmState.NEW, VmState.PROVISION]:
                    command.cores -= vm.cores
                    command.ram -= vm.ram
                    provision_counter += 1
                template = vm.vm_id.split('-')[0]
                if template in templates:
                    if 'spawned' in templates[template]:
                        templates[template]['spawned'] += 1
                    else:
                        templates[template]['spawned'] = 1

            if provision_counter >= 6:
                # don't provision more than 6 VM's at the same time
                return

            for template in list(templates): # make copy of list so that we can edit original
                if 'spawned' in templates[template] and templates[template]['spawned'] >= templates[template]['spawned-max']:
                    del(templates[template]) # we already have the max amount of vms for this template

            if not templates:
                return # max env size reached or no templates defined in config

            if command.cores <= 0 or command.cores < config.schedulerdomain.simplescaler.scaleoutmincoresneeded:
                return

            if command.ram <= 0 or command.ram < config.schedulerdomain.simplescaler.scaleoutminramneeded:
                return

            for template in templates:
                templates[template]['distance'] = templates[template]['ram'] / templates[template]['cores']

            ram_per_core_needed = command.ram / command.cores

            # find best fit based on templates

            # first we calculate the distance based on optimal mem / core distribution
            distances = {}
            for template in templates:
                distance = abs(templates[template]['distance'] - ram_per_core_needed)
                if distance not in distances:
                    distances[distance] = []
                distances[distance].append(template)

            templates = distances[min(distances)] # get templates with least distance

            # now find the templates with resources that best fit what we need
            # we simply select the best fitting template with the most resources
            template = min(templates, key=lambda el: (command.cores - el['cores']) + (command.ram - el['ram']))

            #template = min(templates, key=lambda key: abs(templates[key]['distance'] - ram_per_core_needed))

            # scaleout by one instance
            cloudService = strongr.core.domain.clouddomain.CloudDomain.cloudService()
            cloudCommandFactory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()
            cloudProviderName = config.clouddomain.driver
            profile = getattr(config.clouddomain, cloudProviderName).default_profile if 'profile' not in templates[template] else templates[template]['profile']
            deployVmsCommand = cloudCommandFactory.newDeployVmsCommand(names=[template + '-' + str(uuid.uuid4())], profile=profile, cores=templates[template]['cores'], ram=templates[template]['ram'])

            cloudCommandBus = cloudService.getCommandBus()

            logger.info('Deploying VM {0} cores={1} ram={2}GiB'.format(deployVmsCommand.names[0], deployVmsCommand.cores, deployVmsCommand.ram))

            cloudCommandBus.handle(deployVmsCommand)
