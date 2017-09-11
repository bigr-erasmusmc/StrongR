import strongr.core
import json

class FindNodeWithAvailableResourcesHandler:
    def __call__(self, query):
        core = strongr.core.getCore()
        cache = core.cache()
        if not cache.exists('nodes'):
            with open("/tmp/strongr-nodes", "r") as file:
                nodes = json.loads(file.read())
            for node in nodes:
                nodes[node]["ram_available"] = nodes[node]["ram"]
                nodes[node]["cores_available"] = nodes[node]["cores"]
            cache.set("nodes", nodes, 3600)
            print(nodes)
        else:
            nodes = cache.get('nodes')

        ordered = sorted(nodes, key=lambda key: nodes[key]["ram_available"])

        for node in ordered:
            from pprint import pprint
            pprint(node)
            if nodes[node]["ram_available"] - query.ram >= 0 and nodes[node]["cores_available"] - query.cores >= 0:
                print('Found node!')
                return node

        print('Could not find node for job RAM:{} CORES:{}'.format(query.ram, query.cores))

        return None # TODO: throw exception instead of returning None
