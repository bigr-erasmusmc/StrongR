import strongr.core
import strongr.core.gateway

class ScaleOutHandler(object):
    def __call__(self, command):
        config = strongr.core.Core.config()
        cache = strongr.core.gateway.Gateway.cache()

        if cache.exists('scaleout'):
            scaleout = cache.get('scaleout')
            command.cores -= scaleout['cores']
            command.ram -= scaleout['ram']

        if command.cores <= 0 or command.cores < config.schedulerdomain.simplescaler.scaleoutmincoresneeded:
            return

        if command.ram <= 0 or command.ram < config.schedulerdomain.simplescaler.scaleoutminramneeded:
            return
