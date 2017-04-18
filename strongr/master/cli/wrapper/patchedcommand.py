from cleo import Command

class PatchedCommand(Command):
    def ask(self, question, default):
        # since cleo has a bug that causes it not to return default values we need a wrapper that does exactly that
        output = super(PatchedCommand, self).ask(question)
        if output is None:
            output = default
        return output

    def choice(self, question, options, default):
        # for some reason cleo can not handle arrays with 1 el so we need a workaround
        if len(options) > 1:
            output = super(PatchedCommand, self).choice(question, options, default)
        else:
            output = options[0]

        return output

