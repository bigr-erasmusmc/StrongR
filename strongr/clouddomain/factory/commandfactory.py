from strongr.clouddomain.command import DeployVms, RunShellCode, DestroyVms

from strongr.core.exception import InvalidParameterException

class CommandFactory:
    """ This factory instantiates command objects to be sent to a cloud commandbus. """

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

    def newRunShellCodeCommand(self, sh, host):
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
        elif not len(sh) > 0:
            raise InvalidParameterException('Shellcode {0} is invalid'.format(sh))

        return RunShellCode(sh=sh, host=host)
