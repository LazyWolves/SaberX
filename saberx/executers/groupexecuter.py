from saberx.executers.actionexecuter import ActionExecuter

class GroupExecuter(object):
    
    @staticmethod
    def execute_group(**kwargs):
        group = kwargs.get("group")
        thread_lock = kwargs.get("thread_lock")
        logger = kwargs.get("logger")

        if not GroupExecuter.sanitize(group):
            return False

        group_name = group.get("groupname")
        actions = group.get("actions")

        for action in actions:
            success = ActionExecuter.execute_action(action=action, thread_lock=thread_lock, logger=logger)

            if not success:

                '''
                    Log which action failed
                '''
                if logger:
                    logger.critical("Action {actionname} failed, hence group {groupname} will be marked as failed".format(actionname=action.get("actionname"), groupname=group_name))
                return False

        return True

    @staticmethod
    def sanitize(group):
        return True
