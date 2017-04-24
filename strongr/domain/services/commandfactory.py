from strongr.domain.commands import DeployVm, DeployVms, ListDeployedVms, RunShellCode

from strongr.domain.exceptions import InvalidParameterException

class CommandFactory:
    """ This factory instantiates command objects to be sent to a commandbus. """

    def newDeployVmCommand(self, name, cores, ram):
        """ Generates a new DeployVm command

        :param name: The name of the VM to be deployed
        :param cores: The amount of cores in the VM
        :param ram: The amount of RAM in GiB in the VM

        :type name: string
        :type cores: int
        :type ram: int

        :returns: A DeployVm command object
        :rtype: DeployVm
        """
        if not len(name) > 0:
            raise InvalidParameterException('Name {0} is invalid'.format(name))
        elif not cores > 0:
            raise InvalidParameterException('Cores should be higher than 0')
        elif not ram > 0:
            raise InvalidParameterException('Ram should be higher than 0')

        return DeployVm(name=name, cores=cores, ram=ram)

    def newDeployVmsCommand(self, deployVmCommands):
        """ Generates a new DeployVms command

        :param deployVmCommands: A list of deployVm commands

        :type name: list

        :returns: A DeployVms command object
        :rtype: DeployVms
        """
        for deployCommand in deployVmCommands:
            if not isinstance(deployCommand, DeployVm):
                raise InvalidParameterException('Object {0} should be instance of DeployVm'.format(deployCommand))
        return DeployVms(deployVmCommands)

    def newListDeployedVmsCommand(self):
        """ Generates a new ListDeployedVms command

        :returns: A ListDeployedVms command object
        :rtype: ListDeployedVms
        """
        return ListDeployedVms()

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
