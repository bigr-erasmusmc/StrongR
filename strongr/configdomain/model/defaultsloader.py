class DefaultsLoader:
    def getConfig(self):
        return {
            'internal': {
                'configloaderorder': ['IniLoader', 'JsonLoader', 'YamlLoader']
            },
            'cache': {
                'driver': 'local',
                'namespace': 'strongr-cache-'
            },
            'clouddomain': {
                'driver': 'MockCloud',
                'OpenNebula': {
                    'salt_config': '/etc/salt'
                }
            },
            'restdomain': {
                'backend': 'flask',
                'flask': {
                    'host': '127.0.0.1',
                    'port': 8080,
                    'debug': True
                },
                "gunicorn": {
                    "bind": "0.0.0.0:8080",
                    "worker_class": "sync"
                }
            },
            'schedulerdomain': {
                'driver': 'simplescaler',
                'simplescaler': {
                    'scaleoutmincoresneeded': 16,
                    'scaleoutminramneeded': 16
                }
            },
            'logger': {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'standard': {
                        'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                    }
                },
                'handlers': {
                    'default': {
                        'level': 'INFO',
                        'formatter': 'standard',
                        'class': 'logging.StreamHandler'
                    }
                },
                'loggers': {
                    '': {
                        'handlers': [
                            'default'
                        ],
                        'level': 'INFO',
                        'propagate': True
                    }
                }
            }
        }
