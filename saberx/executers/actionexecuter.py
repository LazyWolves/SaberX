class ActionExecuter(object):

    @staticmethod
    def action_executer(action):
        if not ActionExecuter.sanitize(action):
            return False
        
        trigger = action.get("trigger")
        execute = action.get("execute")
        
    @staticmethod
    def sanitize(action):
        return True
