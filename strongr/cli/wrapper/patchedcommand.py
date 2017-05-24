from cleo import Command

class PatchedCommand(Command):
    def __init__(self, coreContainer):
        self._coreContainer = coreContainer
        super(PatchedCommand, self).__init__()

    def getDomains(self):
        return self._coreContainer.domains()

    def getContainer(self):
        return self._coreContainer

    def ask(self, question, default):
        # since cleo has a bug that causes it not to return default values we need a wrapper that does exactly that
        output = super(PatchedCommand, self).ask(question)
        if output is None:
            output = default
        return output

    def choice(self, question, options, defaultIndex):
        # for some reason cleo can not handle arrays with 1 el so we need a workaround
        if len(options) > 1:
            output = super(PatchedCommand, self).choice(question, options, defaultIndex)
        else:
            output = options[0]

        return output
