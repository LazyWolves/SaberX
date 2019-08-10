class ActionExecuter(object):

    @staticmethod
    def action_executer(action):
        if not ActionExecuter.sanitize(action):
            return False

        trigger_map = {
            "FILE_TRIGGER": ActionExecuter.handle_file_trigger,
            "PROCESS_TRIGGER": ActionExecuter.handle_process_triger,
            "TCP_TRIGGER": ActionExecuter.handle_tcp_trigger,
            "CPU_TRIGGER": ActionExecuter.handle_cpu_trigger,
            "MEMORY_TRIGGER": ActionExecuter.handle_memory_trigger
        }

        action_name = action.get("action_name")
        trigger = action.get("trigger")
        execute = action.get("execute")

        return trigger_map.get(trigger.get("type"))(action_name=action_name, trigger=trigger, execute=execute)
        
    @staticmethod
    def sanitize(action):
        return True
