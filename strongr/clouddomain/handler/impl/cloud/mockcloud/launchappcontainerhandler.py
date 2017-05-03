from strongr.clouddomain.handler.abstract.cloud import AbstractLaunchAppContainerHandler

from strongr.clouddomain.event import AppContainerLaunched

class LaunchAppContainerHandler(AbstractLaunchAppContainerHandler):
    def __call__(self, command):
        containerLaunchedEvent = AppContainerLaunched()
        self.executeAndPublishDomainEvent(event=containerLaunchedEvent, callable=lambda: None)
