class DeployVm:
    # TODO: we should do propper input checking
    def name(self, name):
        self.name = name
        return self

    def cores(self, cores):
        self.cores = cores
        return self

    def ram(self, ram):
        self.ram = ram
        return self