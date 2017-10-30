class ScheduleJob:
    def __init__(self, job_id, cmd, cores, ram):
        self.job_id = job_id
        self.cmd = cmd
        self.cores = cores
        self.ram = ram
