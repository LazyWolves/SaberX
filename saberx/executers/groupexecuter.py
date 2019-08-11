from saberx.executers.actionexecuter import ActionExecuter

class GroupExecuter(object):
    
    @staticmethod
    def execute_group(group):
        if not GroupExecuter.sanitize(group):
            return False

        group_name = group.get("group_name")
        actions = group.get("actions")

        for action in actions:
            success = ActionExecuter.execute_action(action)

            if not success:
                '''
                    Log which action failed
                '''
                return False

        return True

    @staticmethod
    def sanitize(group):
        return True
