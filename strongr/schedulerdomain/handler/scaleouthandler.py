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

            for vm in active_vms:
                if vm.state in [VmState.NEW, VmState.READY]:
                    command.cores -= vm.cores
                    command.ram -= vm.ram
                template = vm.vm_id.split('-')[0]
                if template in templates:
                    if 'spawned' in templates[template]:
                        templates[template]['spawned'] += 1
                    else:
                        templates[template]['spawned'] = 1

            for template in list(templates): # make copy of list so that we can edit original
                if 'spawned' in templates[template] and templates[template]['spawned'] >= templates[template]['spawned-max']:
                    del(templates[template]) # we already have the max amount of vms for this template

            from pprint import pprint
            pprint(templates)

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
            template = min(templates, key=lambda key: abs(templates[key]['distance'] - ram_per_core_needed))

            # scaleout by one instance
            cloudService = strongr.core.domain.clouddomain.CloudDomain.cloudService()
            cloudCommandFactory = strongr.core.domain.clouddomain.CloudDomain.commandFactory()
            cloudProviderName = config.clouddomain.driver
            profile = getattr(config.clouddomain, cloudProviderName).default_profile if 'profile' not in templates[template] else templates[template]['profile']
            deployVmsCommand = cloudCommandFactory.newDeployVmsCommand(names=[template + '-' + str(uuid.uuid4())], profile=profile, cores=templates[template]['cores'], ram=templates[template]['ram'])

            cloudCommandBus = cloudService.getCommandBus()

            logger.info('Deploying VM {0} cores={1} ram={2}GiB'.format(deployVmsCommand.names[0], deployVmsCommand.cores, deployVmsCommand.ram))

            #cloudCommandBus.handle(deployVmsCommand)
