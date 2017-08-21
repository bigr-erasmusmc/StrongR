from strongr.restdomain.api.apiv1 import blueprint as apiv1

class RetrieveBlueprintsHandler:
    def __call__(self, command):
        # return a list of blueprints
        return [apiv1]
