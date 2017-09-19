import strongr.core
from strongr.core.gateways import Gateways


class ClaimResourcesOnNodeHandler:
    def __call__(self, command):
        core = strongr.core.getCore()
        cache = Gateways.cache()
        if cache.exists('nodes'):
            nodes = cache.get("nodes")
            nodes[command.node]["ram_available"] -= command.ram
            nodes[command.node]["cores_available"] -= command.cores
            cache.set('nodes', nodes, 3600)
