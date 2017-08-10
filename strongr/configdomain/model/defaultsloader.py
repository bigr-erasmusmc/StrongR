class DefaultsLoader:
    def getConfig(self):
        return {
            'internal.configloaderorder': 'IniLoader, JsonLoader'
        }
