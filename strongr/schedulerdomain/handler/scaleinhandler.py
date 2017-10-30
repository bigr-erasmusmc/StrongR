import strongr.core
import strongr.core.gateways

import logging

class ScaleOutHandler(object):
    def __call__(self, command):
        if strongr.core.gateways.Gateways.lock('scaleout-lock').exists():
            return # only every run one of these commands at once

        with strongr.core.gateways.Gateways.lock('scaleout-lock'):  # only ever run one of these commands at once
            config = strongr.core.Core.config()
            cache = strongr.core.gateways.Gateways.cache()
            logger = logging.getLogger('schedulerdomain.' + self.__class__.__name__)

            if cache.exists('scaleout'):
                scaleout = cache.get('scaleout')
