import strongr.core

class FindNodeWithAvailableResourcesHandler:
    def __call__(self, query):
        cache = core.Core.cache()
        if cache.exists('asd'):
            pass
