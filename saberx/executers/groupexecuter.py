from saberx.executers.actionexecuter import ActionExecuter

class GroupExecuter(object):
    
    @staticmethod
    def execute_group(**kwargs):
        group = kwargs.get("group")
        thread_lock = kwargs.get("thread_lock")

        if not GroupExecuter.sanitize(group):
            return False

        group_name = group.get("group_name")
        actions = group.get("actions")

        for action in actions:
            success = ActionExecuter.execute_action(action=action, thread_lock=thread_lock)

            if not success:
                '''
                    Log which action failed
                '''
                return False

        return True

    @staticmethod
    def sanitize(group):
        return True
