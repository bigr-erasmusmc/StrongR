from strongr.schedulerdomain.command import ScheduleTask, DoDelayedTasks,\
                                            ClaimResourcesOnNode, ReleaseResourcesOnNode,\
                                            StartTaskOnNode

from strongr.core.exception import InvalidParameterException

class CommandFactory:
    """ This factory instantiates command objects to be sent to a scheduler commandbus. """
    def newDoDelayedTasks(self):
        """ Generates a new DoDelayedTasks command

        :returns: A DoDelayedTasks command object
        :rtype: DoDelayedTasks
        """
        return DoDelayedTasks()

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

    def newClaimResourcesOnNode(self, node, cores, ram):
        """ Generates a new ClaimResourcesOnNode command

        :param node: the node name
        :type node: string
        :param cores: the amount of cores claimed
        :type cores: int
        :param ram: the amount of ram claimed
        :type ram: int

        :returns: A ClaimResourcesOnNode command object
        :rtype: ClaimResourcesOnNode
        """
        if not len(node) > 0:
            raise InvalidParameterException('Node is invalid')
        elif not cores > 0:
            raise InvalidParameterException('Cores should be higher than 0')
        elif not ram > 0:
            raise InvalidParameterException('Ram should be higher than 0')

        return ClaimResourcesOnNode(node=node,cores=cores, ram=ram)

    def newReleaseResourcesOnNode(self, node, cores, ram):
        """ Generates a new ReleaseResourcesOnNode command

        :param node: the node name
        :type node: string
        :param cores: the amount of cores claimed
        :type cores: int
        :param ram: the amount of ram claimed
        :type ram: int

        :returns: A ReleaseResourcesOnNode command object
        :rtype: ReleaseResourcesOnNode
        """
        if not len(node) > 0:
            raise InvalidParameterException('Node is invalid')
        elif not cores > 0:
            raise InvalidParameterException('Cores should be higher than 0')
        elif not ram > 0:
            raise InvalidParameterException('Ram should be higher than 0')

        return ReleaseResourcesOnNode(node=node,cores=cores, ram=ram)

    def newStartTaskOnNode(self, node, taskid):
        """ Generates a new StartTaskOnNode command

        :param node: the node name
        :type node: string
        :param taskid: the taskid to be started
        :type taskid: string

        :returns: A StartTaskOnNode command object
        :rtype: StartTaskOnNode
        """
        if not len(node) > 0:
            raise InvalidParameterException('node is invalid')
        elif not len(taskid) > 0:
            raise InvalidParameterException('taskid is invalid')

        return StartTaskOnNode(node=node, taskid=taskid)
