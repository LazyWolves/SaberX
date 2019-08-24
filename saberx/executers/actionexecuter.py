from saberx.sabercore.triggers.filetrigger import FileTrigger
from saberx.sabercore.triggers.processtrigger import ProcessTrigger
from saberx.sabercore.triggers.cputrigger import CPUTrigger
from saberx.sabercore.triggers.memorytrigger import MemoryTrigger
from saberx.sabercore.triggers.tcptrigger import TCPTrigger
from saberx.sabercore.shellexecutor import ShellExecutor

class ActionExecuter(object):

    @staticmethod
    def execute_action(action):
        if not ActionExecuter.sanitize(action):
            return False

        trigger_map = {
            "FILE_TRIGGER": FileTrigger,
            "PROCESS_TRIGGER": ProcessTrigger,
            "TCP_TRIGGER": TCPTrigger,
            "CPU_TRIGGER": CPUTrigger,
            "MEMORY_TRIGGER": MemoryTrigger
        }

        action_name = action.get("action_name")
        trigger = action.get("trigger")
        execute = action.get("execute")

        triggerHandler = trigger_map.get(trigger.get("type"))(**trigger)
        triggered, error = triggerHandler.fire_trigger()

        if error:
            '''
                Log the error and return False. Consider the trgger as a failure.
            '''
            return False

        if triggered:
            shellExecuter = ShellExecutor(command_list=execute)
            success = shellExecuter.execute_shell_list()
            return success

        return True

    @staticmethod
    def sanitize(action):
        return True
