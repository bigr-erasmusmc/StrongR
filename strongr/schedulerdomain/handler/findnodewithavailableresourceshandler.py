import strongr.core
#import json

import time

import strongr.core.domain.clouddomain
import strongr.core.gateways


class FindNodeWithAvailableResourcesHandler:
    _machines = {}
    _query_timer = 0

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

        if time.time() > self._query_timer:
            core = strongr.core.getCore()
            cache = strongr.core.gateways.Gateways.cache()
            cloudQueryBus = strongr.core.domain.clouddomain.CloudDomain.cloudService().getCloudServiceByName(core.config().clouddomain.driver).getQueryBus()
            cloudQueryFactory = strongr.core.domain.clouddomain.CloudDomain.queryFactory()

            machines = cloudQueryBus.handle(cloudQueryFactory.newListDeployedVms())
            if machines is not None:
                for machine in machines:
                    if machine.startswith('worker-') and machine not in self._machines:
                        # add new machines
                        self._machines[machine] = machines[machine]
                        self._machines[machine]["ram_available"] = self._machines[machine]["ram"]
                        self._machines[machine]["cores_available"] = self._machines[machine]["cores"]

                for machine in list(self._machines):
                    if machine not in machines:
                        del self._machines[machine] # delete machines that are no longer up

                if cache.exists('nodes'):
                    cached_nodes = cache.get('nodes')
                    for machine in cached_nodes:
                        if machine in self._machines:
                            # sync with cache
                            self._machines[machine]["ram_available"] = cached_nodes[machine]["ram_available"]
                            self._machines[machine]["cores_available"] = cached_nodes[machine]["cores_available"]

                # push back in cache, other commands need this data
                cache.set('nodes', self._machines, 3600)
                self._query_timer = time.time() + 120 # refresh machine list once every 2 minutes

        ordered = sorted(self._machines, key=lambda key: self._machines[key]["ram_available"])

        for machine in ordered:
            if self._machines[machine]["ram_available"] - query.ram >= 0 and self._machines[machine]["cores_available"] - query.cores >= 0:
                return machine


        return None # TODO: throw exception instead of returning None
