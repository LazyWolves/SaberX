"""
.. module:: actionexecuter
   :synopsis: Module for executing an action

"""

from saberx.sabercore.triggers.filetrigger import FileTrigger
from saberx.sabercore.triggers.processtrigger import ProcessTrigger
from saberx.sabercore.triggers.cputrigger import CPUTrigger
from saberx.sabercore.triggers.memorytrigger import MemoryTrigger
from saberx.sabercore.triggers.tcptrigger import TCPTrigger
from saberx.sabercore.shellexecutor import ShellExecutor


class ActionExecuter(object):

    """
        class for handling execution of a given action.
        This class mostly comrises of status function.
    """

    @staticmethod
    def execute_action(**kwargs):

        """
            **Method to execute a given action**

            This method executes a given action. It fires the associated
            trigger using the required trigger handler if trigger is
            successfull, executes the desired commands.

            The layout of a action will be as follows:

            action_name: string
            trigger:
                type: TCP_TRIGGER
                check: tcp_connect | tcp_fail
                host: host_name
                port: port
                negate: true | false
                attemp: number
                threshold: number
                ssl: true | false
            execute:
            - command1
            - command2

            Args:
                kwargs : Object containing action, thread lock and logger

            Returns:
                bool : Success or failure for this action
        """

        action = kwargs.get("action")
        thread_lock = kwargs.get("thread_lock")
        logger = kwargs.get("logger")

        if not ActionExecuter.sanitize(action):
            return False

        # map associating trigger type with corresponding method
        trigger_map = {
            "FILE_TRIGGER": FileTrigger,
            "PROCESS_TRIGGER": ProcessTrigger,
            "TCP_TRIGGER": TCPTrigger,
            "CPU_TRIGGER": CPUTrigger,
            "MEMORY_TRIGGER": MemoryTrigger
        }

        action_name = action.get("actionname")
        trigger = action.get("trigger")
        execute = action.get("execute")

        triggerHandler = trigger_map.get(trigger.get("type"))(**trigger)
        triggered, error = triggerHandler.fire_trigger()

        if error:

            '''
                Log the error and return False. Consider the trgger as a
                failure.
            '''

            if logger:
                logger.critical(
                    "Action {actionname} failed with error : {error}"
                    .format(actionname=action_name, error=str(error)))

            return False

        if triggered:

            '''
                If triggered, desired commands are executed using
                shell executer.
            '''
            shellExecuter = ShellExecutor(command_list=execute, logger=logger)
            with thread_lock:
                success = shellExecuter.execute_shell_list()
            return success

        return True

    @staticmethod
    def sanitize(action):
        return True
