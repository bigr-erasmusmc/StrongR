class VMConfiguration:
    # ram in GiB
    # cores in number of processing cores
    def __init__(self, cores = None, ram = None):
        self.cores = cores
        self.ram = ram
