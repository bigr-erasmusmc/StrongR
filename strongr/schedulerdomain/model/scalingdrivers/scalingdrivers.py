import dependency_injector.containers as containers
import dependency_injector.providers as providers

import strongr.core

from strongr.schedulerdomain.model.scalingdrivers.simplescaler import ScaleIn as SimpleScaleIn, ScaleOut as SimpleScaleOut

class ScalingDrivers(containers.DeclarativeContainer):
    """IoC container of service providers."""
    _scalingdrivers = providers.Object({
        'simplescaler': {
            'scalein': SimpleScaleIn,
            'scaleout': SimpleScaleOut
        }
    })

    scalein_driver = providers.Singleton(_scalingdrivers()[strongr.core.Core.config().schedulerdomain.scalingdriver]['scalein'], dict(strongr.core.Core.config().schedulerdomain.as_dict()[strongr.core.Core.config().schedulerdomain.scalingdriver]))
    scaleout_driver = providers.Singleton(_scalingdrivers()[strongr.core.Core.config().schedulerdomain.scalingdriver]['scaleout'], dict(strongr.core.Core.config().schedulerdomain.as_dict()[strongr.core.Core.config().schedulerdomain.scalingdriver]))
