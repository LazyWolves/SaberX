"""
.. module:: filetrigger
   :synopsis: Module for firing file trigger.
"""

from .triggerbase import TriggerBase
from .filehandler import FileHandler


class FileTrigger(TriggerBase):

    """
        **Class for creating file trigger**
    """
    def __init__(self, **kwargs):

        """
            **Method for initialing File trigger**

        """
        super(FileTrigger, self).__init__(
            type=kwargs.get("type"), 
            check=kwargs.get("check"), 
            negate=kwargs.get("negate"))

        if kwargs.get("regex"):
            self.regex = kwargs.get("regex")

        if kwargs.get("path"):
            self.path = kwargs.get("path")
        self.position = kwargs.get("position", "tail")
        self.limit = kwargs.get("limit", 50)

        self.valid_checks = ["empty", "present", "regex"]
        self.valid_positions = ["head", "tail"]

    def fire_trigger(self):

        """
            **Method to fire the trigger**

            This method first sanitises the parameters, calls file handler
            to evaluate the trigger conditions and returns trigger status

            Returns:
                bool : Trigger fired or not
        """
        if not self.sanitise():
            return False, "IMPROPER_ARGUMENTS"

        if self.check == "present":
            triggered, error = FileHandler.is_present(self.path)
            return self.eval_negate(triggered, error)

        if self.check == "empty":
            triggered, error = FileHandler.is_empty(self.path)
            return self.eval_negate(triggered, error)

        if self.check == "regex":
            triggered, error = FileHandler.search_keyword(
                path=self.path, 
                limit=self.limit, 
                position=self.position, 
                regex=self.regex)
            return self.eval_negate(triggered, error)

    def sanitise(self):
        if not self.path:
            '''
                Log error
            '''
            return False

        if not self.type:
            '''
                Log the error
            '''
            return False

        if not self.check:
            '''
                Log error
            '''
            return False

        if not (self.check in self.valid_checks):
            '''
                Log error
            '''
            return False

        if self.limit and self.limit <= 0:
            '''
                Log error
            '''
            return False

        if self.position and not (self.position in self.valid_positions):
            '''
                Log error
            '''
            return False

        return True
