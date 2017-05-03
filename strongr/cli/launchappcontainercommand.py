from .wrapper import Command

class LaunchAppContainerCommand(Command):
    """
    Deploys a docker container in the cloud. A first step towards elasticity.

    deploy:single
    """
    def handle(self):
        services = self.getServicesContainer()
        cloudServices = services.cloudServices()
        commandFactory = services.cloudCommandFactory()
