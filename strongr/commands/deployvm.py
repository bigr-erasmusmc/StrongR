class DeployVm:
    # TODO: we should do propper input checking
    def __init__(self, name, cores, ram):
        self.name = name
        self.cores = cores
        self.ram = ram
