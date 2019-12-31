"""
    module:: shellexecuter
   :synopsis: Module for executing shell commands
"""

import subprocess


class ShellExecutor:

    """
        **Class for executing shell commands**
    """

    def __init__(self, **kwargs):

        """
            **Method to initialise shellexecuter**

            Args:
                kwargs (dict): dict containing command list and logger object
        """
        self.command_list = kwargs.get("command_list")
        self.logger = kwargs.get("logger")

    def execute_shell_single(self, command):

        """
            **Method for executing a single shell command**

            This method executes a single shell command

            Args:
                command (string): command tp be exeuted

            Returns:
                bool, output, proc_exit_code: status of the command execution, output of the command, return code

        """

        '''
            TODO:
                sanity check
        '''
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, errors = proc.communicate()
        proc_exit_code = proc.returncode

        if proc_exit_code != 0:

            if self.logger:
                self.logger.critical("Shell executer failed with error : {errors}".format(errors=errors))
            return False, errors, proc_exit_code

        return True, output, proc_exit_code

    def execute_shell_list(self):

        """
            **Method for executing a list of shell commands**

            This method executes a list of shell commands.

            It is to be notes that, if a single command fails, the remaning commands
            adter the failed command will be ignored.

            Returns:
                bool: status of execution of the commands.
        """
        for command in self.command_list:

            # log the command being executed

            success, reponse, proc_exit_code = self.execute_shell_single(command)
            if not success:
                # log the response and proc_exit_code
                return False

            # log the response and proc_exit_code

        return True
