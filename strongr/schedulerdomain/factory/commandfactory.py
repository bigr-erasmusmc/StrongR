from strongr.schedulerDomain.command import ScheduleTask

from strongr.core.exception import InvalidParameterException

class CommandFactory:
    """ This factory instantiates command objects to be sent to a scheduler commandbus. """

    def newScheduleTaskCommand(self, taskid, cmd, cores, ram):
        """ Generates a new ScheduleTask command

        :param taskid: the taskid
        :param cmd: The shellcode to be run
        :param cores: The amount of cores in the VM
        :param ram: The amount of RAM in GiB in the VM

        :type taskid: string
        :type cmd: string
        :type cores: int
        :type ram: int

        :returns: A DeployVm command object
        :rtype: DeployVm
        """
        if not len(cmd) > 0:
            raise InvalidParameterException('Cmd {0} is invalid'.format(cmd))
        elif not cores > 0:
            raise InvalidParameterException('Cores should be higher than 0')
        elif not ram > 0:
            raise InvalidParameterException('Ram should be higher than 0')
        elif not len(taskid) > 0:
            raise InvalidParameterException('Taskid invalid')

        return ScheduleTask(taskid=taskid, cmd=cmd, cores=cores, ram=ram)
