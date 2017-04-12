from cmndr.commandbus import CommandBus
from cmndr.handlers import CommandHandler
from cmndr.handlers.inflectors import CallableInflector
from cmndr.handlers.locators import InMemoryLocator
from cmndr.handlers.nameextractors import ClassNameExtractor

from dto.vm.configuration import VMConfiguration
from commands import DeployVm
from commandhandlers.cloud.opennebula import DeployVmHandler



extractor = ClassNameExtractor()
locator = InMemoryLocator({DeployVmHandler(): DeployVm.__name__})
inflector = CallableInflector()
handler = CommandHandler(extractor, locator, inflector)
commandBus = CommandBus([handler])


config = VMConfiguration(1, 4)
deployVmCommand = DeployVm() \
    .name('thomas-test-deploy') \
    .configuration(config)
commandBus.handle(deployVmCommand)
