from strongr.schedulerdomain.command import ScheduleJob, DoDelayedTasks,\
                                            ClaimResourcesOnNode, ReleaseResourcesOnNode,\
                                            StartJobOnVm, CheckJobRunning,\
                                            EnsureMinAmountOfNodes, ScaleOut

from strongr.core.exception import InvalidParameterException

class CommandFactory:
    """ This factory instantiates command objects to be sent to a scheduler commandbus. """
    def newScaleOut(self, cores, ram):
        if not cores > 0:
            raise InvalidParameterException('Cores should be higher than 0')
        elif not ram > 0:
            raise InvalidParameterException('Ram should be higher than 0')

        return ScaleOut(cores, ram)

    def newEnsureMinAmountOfNodes(self):
        return EnsureMinAmountOfNodes()

    def newDoDelayedTasks(self):
        """ Generates a new DoDelayedTasks command

        :returns: A DoDelayedTasks command object
        :rtype: DoDelayedTasks
        """
        return DoDelayedTasks()

    def newScheduleJobCommand(self, job_id, cmd, cores, ram):
        """ Generates a new ScheduleTask command

        :param job_id: the jobs id (max 32 characters)
        :param cmd: The shellcode to be run
        :param cores: The amount of cores in the VM
        :param ram: The amount of RAM in GiB in the VM

        :type job_id: string
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
        elif not len(job_id) > 0:
            raise InvalidParameterException('Taskid invalid')

        return ScheduleJob(job_id=job_id, cmd=cmd, cores=cores, ram=ram)

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

    def newStartJobOnVm(self, vm_id, job_id):
        """ Generates a new StartJobOnVm command

        :param vm_id: the node name
        :type vm_id: string
        :param job_id: the taskid to be started
        :type job_id: string

        :returns: A StartJobOnVm command object
        :rtype: StartJobOnVm
        """
        if not len(vm_id) > 0:
            raise InvalidParameterException('node is invalid')
        elif not len(job_id) > 0:
            raise InvalidParameterException('taskid is invalid')

        return StartJobOnVm(vm_id=vm_id, job_id=job_id)

    def newCheckJobRunning(self, job_id):
        """ Generates a new CheckJobRunning command

        :param node: the node name
        :type node: string
        :param job_id: the taskid to be started
        :type job_id: string

        :returns: A CheckJobRunning command object
        :rtype: CheckJobRunning
        """
        if not len(job_id) > 0:
            raise InvalidParameterException('taskid is invalid')

        return CheckJobRunning(job_id=job_id)
