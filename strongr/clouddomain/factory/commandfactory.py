from strongr.clouddomain.command import DeployVms, RunShellCode, DestroyVms, JobFinished

from strongr.core.exception import InvalidParameterException

class CommandFactory:
    """ This factory instantiates command objects to be sent to a cloud commandbus. """

    def newJobFinishedCommand(self, job_id, ret, retcode):
        """ Generates a new JobFinished command

        :param job_id: An identifier token for the job
        :type job_id: string

        :param ret: Usually the stdout of the job
        :type ret: string

        :param retcode: The exit code of the job
        :type ret: int

        :returns: A JobFinished command object
        :rtype: JobFinished
        """
        if not isinstance(job_id, basestring) or len(job_id.strip()) == 0:
            raise InvalidParameterException('jid is invalid')
        elif not isinstance(ret, basestring) or len(ret.strip()) == 0:
            raise InvalidParameterException('ret is invalid')
        elif not isinstance(retcode, int):
            raise InvalidParameterException('retcode is invalid')

        return JobFinished(job_id, ret, retcode)

    def newDestroyVmsCommand(self, names):
        """ Generates a new DestroyVm command

        :param name: The name of the VM to be destroyed
        :type name: string

        :returns: A DestroyVm command object
        :rtype: DestroyVm
        """
        if not isinstance(names, list) or len(names) <= 0:
            raise InvalidParameterException('names is invalid')

        return DestroyVms(names=names)

    def newDeployVmsCommand(self, names, profile, cores, ram):
        """ Generates a new DeployVms command

        :param names: A list of names
        :type names: list

        :param profile: the vm profile to be used
        :type profile: string

        :param cores: the number of cores per vm
        :type cores: int

        :param ram: the amount of ram per vm in GiB
        :type ram: int

        :returns: A DeployVms command object
        :rtype: DeployVms
        """

        if not isinstance(names, list) or len(names) <= 0:
            raise InvalidParameterException('names is inavlid')

        if not isinstance(cores, int) or cores <= 0:
            raise InvalidParameterException('cores is inavlid')

        if not isinstance(ram, int) or ram <= 0:
            raise InvalidParameterException('ram is invalid')

        if len(profile) <= 0:
            raise InvalidParameterException('profile is invalid')

        return DeployVms(names, profile, cores, ram)

    def newRunShellCodeCommand(self, job_id, sh, host):
        """ Generates a new RunShellCode command

        :param sh: runShellCode
        :type sh: string
        :param host: The hostname where the shellcode should be executed or '*' to execute on all hosts
        :type host: string

        :returns: A new RunShellCode command object
        :rtype: RunShellCodeCommand
        """
        if not len(host) > 0:
            raise InvalidParameterException('Host {0} is invalid'.format(host))
        elif not len(job_id) > 0:
            raise InvalidParameterException('job_id is invalid')
        elif not len(sh) > 0:
            raise InvalidParameterException('Shellcode {0} is invalid'.format(sh))

        return RunShellCode(job_id=job_id, sh=sh, host=host)
