"""
.. module:: groupexecuter
   :synopsis: Module for executing a group of actions.

"""

from saberx.executers.actionexecuter import ActionExecuter


class GroupExecuter(object):

    """
        **Class for handling executing of a group of actions**
    """

    @staticmethod
    def execute_group(**kwargs):

        """
            **Method for executing a group of actions**

            This method takes a group of actions. It then ieterates over thoses
            group actions and executes them one by one using the required
            actionexecuter module.

            It is important to be noted here that actions in a group are
            executed synchronously, and if one action in the pipeline fails,
            ie, triggered but command executions fails due to some excpetion
            or error, the entire pipeline after the failed action is ignored.

            If you dont wont the above dependency between your actions, it is
            advised to place the actions in different groups. Groups have no
            such dependencies are executed concurrently.
        """
        group = kwargs.get("group")
        thread_lock = kwargs.get("thread_lock")
        logger = kwargs.get("logger")

        if not GroupExecuter.sanitize(group):
            return False

        group_name = group.get("groupname")
        actions = group.get("actions")

        for action in actions:
            success = ActionExecuter.execute_action(
                action=action, thread_lock=thread_lock, logger=logger)

            if not success:

                '''
                    Log which action failed
                '''
                if logger:
                    logger.critical("Action {actionname} failed, hence "
                                    "group {groupname} will be marked as "
                                    "failed"
                                    .format(actionname=action.get(
                                        "actionname"), groupname=group_name))
                return False

        return True

    @staticmethod
    def sanitize(group):
        return True
