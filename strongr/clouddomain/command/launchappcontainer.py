class LaunchAppContainer():
    def __init__(self, host, image, ram, swap, affinity):
        self.host = host
        self.image = image
        self.ram = ram
        self.swap = swap
        self.affinity = affinity
