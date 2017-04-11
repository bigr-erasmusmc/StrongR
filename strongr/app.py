from commandr.handlers.commandhandler import CommandHandler
from commandr.handlers.inflectors.callableinflector import CallableInflector
from commandr.handlers.locators.inmemorylocator import InMemoryLocator
from commandr.handlers.nameextractors.classnameextractor import ClassNameExtractor
from commandr.commandbus import CommandBus

from dto.vm.configuration import VMConfiguration
from commands import DeployVM


config = VMConfiguration(1, 4, False)
deployVmCommand = DeployVM() \
    .name('thomas-test-deploy') \
    .configuration(config)

extractor = ClassNameExtractor()
locator = InMemoryLocator({TestCommandHandler(): TestCommand.__name__})
inflector = CallableInflector()
handler = CommandHandler(extractor, locator, inflector)
a = CommandBus([Middleware1(), Middleware2(), handler])
print(a.handle(TestCommand({"a": 1, "b": 2})))
