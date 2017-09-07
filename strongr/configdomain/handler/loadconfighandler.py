from strongr.configdomain.model import DefaultsLoader, IniLoader, JsonLoader

class LoadConfigHandler():
    def __call__(self, command):
        config = DefaultsLoader().getConfig()

        loaders = {
            IniLoader.__name__: IniLoader(),
            JsonLoader.__name__: JsonLoader(),
        }

        loadOrder = [x.strip() for x in config['internal.configloaderorder'].split(',') if x.strip() != '']
        for loaderName in loadOrder:
            if loaderName in loaders:
                config.update(loaders[loaderName].getConfig(command.environment))
                # update config in core many times as config loaders can use config parameters from other loaders
                # example: a database configloader that needs credentials
                from strongr.core.core import core
                core.config.update(config)
            else:
                # fatal error
                # since the loadOrder is hardcoded in the defaultsloader it should always work. If not,
                # it is considered a fatal error.
                raise Exception("Invalid config loader!")

