import strongr.core

import time

import strongr.core.domain.clouddomain
import strongr.core.gateways

from strongr.core.lock.redislock import RedisLock


class FindNodeWithAvailableResourcesHandler:
    _timeout = 0

    def __call__(self, query):
        #core = strongr.core.getCore()
        #cache = core.cache()
        #if not cache.exists('nodes'):
        #    with open("/tmp/strongr-nodes", "r") as file:
        #        nodes = json.loads(file.read())
        #    for node in nodes:
        #        nodes[node]["ram_available"] = nodes[node]["ram"]
        #        nodes[node]["cores_available"] = nodes[node]["cores"]
        #    cache.set("nodes", nodes, 3600)
        #    print(nodes)
        #else:
        #    nodes = cache.get('nodes')
        #

        core = strongr.core.Core
        cache = strongr.core.gateways.Gateways.cache()

        cloudQueryBus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getCloudServiceByName(core.config().clouddomain.driver).getQueryBus()
        cloudQueryFactory = strongr.core.domain.clouddomain.CloudDomain.queryFactory()

        if not cache.exists('nodes'):
            machines = cloudQueryBus.handle(cloudQueryFactory.newListDeployedVms())
            nodes = {}
            if machines is not None:
                for machine in machines:
                    if machine.startswith('worker-'):
                        # add new machines
                        nodes[machine] = machines[machine]
                        nodes[machine]["ram_available"] = nodes[machine]["ram"]
                        nodes[machine]["cores_available"] = nodes[machine]["cores"]
            # push back in cache, other commands need this data
            cache.set('nodes', nodes, 3600)
            self._timeout = int(time.time()) + 120
        elif int(time.time()) > self._timeout:
            machines = cloudQueryBus.handle(cloudQueryFactory.newListDeployedVms())
            nodes = cache.get('nodes')
            if machines is not None:
                for machine in machines:
                    if machine.startswith('worker-') and machine not in nodes:
                        # add new machines
                        nodes[machine] = machines[machine]
                        nodes[machine]["ram_available"] = nodes[machine]["ram"]
                        nodes[machine]["cores_available"] = nodes[machine]["cores"]

            for node in list(nodes):
                if node not in machines:
                    del nodes[machine]  # delete machines that are no longer up

            # push back in cache, other commands need this data
            cache.set('nodes', nodes, 3600)
            self._timeout = int(time.time()) + 120 # refresh every 2 minutes
        else:
            nodes = cache.get('nodes')


        ordered = sorted(nodes, key=lambda key: nodes[key]["ram_available"])

        for machine in ordered:
            if 'locked' not in nodes[machine] and nodes[machine]["ram_available"] - query.ram >= 0 and nodes[machine]["cores_available"] - query.cores >= 0:
                return machine


        return None # TODO: throw exception instead of returning None
