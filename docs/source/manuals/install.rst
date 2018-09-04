Installing StrongR
******************
StrongR currently supports two cloud-adapters. The OpenNebula and MockCloud adapters.

OpenNebula
==========

MockCloud
=========
The mockcloud is useful for testing containers localy.

Let's clone strongr and install it. Then create a scratch directory.

.. code-block:: shell

  git clone https://gitlab.com/bbmri/infra/strongr.git
  cd strongr
  pip install -r requirements.txt
  pip install -e .
  mkdir /scratch
  chmod 777 /scratch

Now copy over the config below to ~/.strongr/config.json.

.. code-block:: json

  {
    "defaults": {
    },
    "develop": {
      "lock": {
        "driver": "file",
        "file": {
          "path": "/tmp/strongr-locks"
        }
      },
      "cache": {
        "driver": "local"
      },
      "db": {
        "engine": {
          "url": "sqlite:////tmp/strongr.db"
        }
      },
      "clouddomain": {
        "driver": "MockCloud",
        "MockCloud": {
          "scratch": "/scratch"
        }
      },
      "logger": {
        "handlers": {
          "default": {
            "level": "DEBUG"
          }
        },
        "loggers": {
          "": {
            "level": "DEBUG"
          }
        }
      }
    }
  }

Finally, run the mockcloud.

.. code-block:: shell

  strongr r:r
