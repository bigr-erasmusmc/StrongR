from .clouds import OpenNebula
from .clouds import VirtualBox

class CloudServices():
    """IoC container of supported cloud providers."""
    clouds = [ \
        OpenNebula, \
        VirtualBox\
    ]

    def getCloudNames(self):
        return [cloud.__name__ for cloud in self.clouds]

    def getCloudServiceByName(self, name):
        return next((cloud for cloud in self.clouds if cloud.__name__ == name), None)
