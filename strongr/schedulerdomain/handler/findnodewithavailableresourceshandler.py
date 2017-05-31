import strongr.core
import json

class FindNodeWithAvailableResourcesHandler:
    def __call__(self, query):
        cache = strongr.core.Core.cache()
        if not cache.exists('nodes'):
            with open("/tmp/strongr-nodes", "r") as file:
                nodes = json.loads(file.read())
            for node in nodes:
                nodes[node]["ram_available"] = nodes[node]["ram"]
                nodes[node]["cores_available"] = nodes[node]["cores"]
            cache.set("nodes", nodes, 3600)
        else:
            nodes = cache.get('nodes')

        ordered = sorted(nodes, key=lambda key: nodes[key]["ram_available"])

        for node in ordered:
            if nodes[node]["ram_available"] - query.ram >= 0 and nodes[node]["cores_available"] - query.cores >= 0:
                return node

        return None # TODO: throw exception instead of returning None
