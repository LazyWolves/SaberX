"""
.. module:: memorytrigger
   :synopsis: Module for firing memory trigger.
"""

from .triggerbase import TriggerBase
from .memoryhandler import MemoryHandler


class MemoryTrigger(TriggerBase):

    """
        **Class for creating memory trigger**
    """
    def __init__(self, **kwargs):

        """
            **Method for initialing CPU trigger**

        """
        super(MemoryTrigger, self).__init__(
            type=kwargs.get("type"),
            check=kwargs.get("check"),
            negate=kwargs.get("negate"))

        self.attr = kwargs.get("attr", "used")
        self.operation = kwargs.get("operation", ">")

        if kwargs.get("threshold") is not None:
            self.threshold = kwargs.get("threshold")

        self.valid_checks = ["virtual", "swap"]
        self.valid_attrs = ["used", "available", "free"]
        self.valid_operations = ["=", "<", ">", "<=", ">="]

    def fire_trigger(self):

        """
            **Method to fire the trigger**

            This method first sanitises the parameters, calls memory handler
            to evaluate the trigger conditions and returns trigger status

            Returns:
                bool : Trigger fired or not
        """
        if not self.sanitise():
            return False, "INVALID_ARGUMENTS"

        triggered, error = MemoryHandler.check_mem(
            check_type=self.check,
            attr=self.attr,
            operation=self.operation,
            threshold=self.threshold)
        return self.eval_negate(triggered, error)

    def sanitise(self):

        """
            **Method to check validity of the params**

            Returns:
                bool : params are proper or not
        """
        if not self.check:

            '''
                Log error
            '''
            return False

        if not self.type:

            '''
                Log error
            '''
            return False

        if self.check not in self.valid_checks:

            '''
                Log error
            '''
            return False

        if not self.attr:

            '''
                Log error
            '''
            return False

        if self.attr not in self.valid_attrs:

            '''
                Log error
            '''
            return False

        if not self.operation:

            '''
                Log error
            '''
            return False

        if self.operation not in self.valid_operations:

            '''
                Log error
            '''
            return False

        if self.threshold is None:

            '''
                Log error
            '''

            return False

        if type(self.threshold) != float:

            '''
                Log error
            '''

            return False

        return True
