import strongr.core
from strongr.core.gateways import Gateways


class ReleaseResourcesOnNodeHandler:
    def __call__(self, command):
        cache = Gateways.cache()
        if cache.exists('nodes'):
            nodes = cache.get("nodes")
            nodes[command.node]["ram_available"] += command.ram
            nodes[command.node]["cores_available"] += command.cores
            cache.set('nodes', nodes, 3600)
