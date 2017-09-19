import strongr.core
import strongr.core.gateways


class ClaimResourcesOnNodeHandler:
    def __call__(self, command):
        cache = strongr.core.gateways.Gateways.cache()
        if cache.exists('nodes'):
            nodes = cache.get("nodes")
            nodes[command.node]["ram_available"] -= command.ram
            nodes[command.node]["cores_available"] -= command.cores
            cache.set('nodes', nodes, 3600)
