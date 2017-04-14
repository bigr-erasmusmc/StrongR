from .clouds import OpenNebula

class CloudServices():
    clouds = [ \
        OpenNebula
    ]

    def getCloudNames(self):
        return [cloud.__name__ for cloud in self.clouds]

    def getCloudServiceByName(self, name):
        service = next((cloud for cloud in self.clouds if cloud.__name__ == name), None)
        if service == None: return None
        return service()
