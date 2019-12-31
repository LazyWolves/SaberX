"""
.. module:: cputrigger
   :synopsis: Module for firing CPU trigger.
"""

from .triggerbase import TriggerBase
from .cpuhandler import CPUHandler

class CPUTrigger(TriggerBase):

    """
        **Class for creating CPU trigger**
    """

    def __init__(self, **kwargs):

        """
            **Method for initialing CPU trigger**

        """
        super(CPUTrigger, self).__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

        self.operation = kwargs.get("operation", ">")

        if kwargs.get("threshold"):
            self.threshold = kwargs.get("threshold")

        self.valid_operations = ["=", "<", ">", "<=", ">="]
        self.valid_checks = ["loadaverage"]

    def  fire_trigger(self):

        """
            **Method to fire the trigger**

            This method first sanitises the parameters, calls cpu handler
            to evaluate the trigger conditions and returns trigger status

            Returns:
                bool : Trigger fired or not
        """
        if not self.sanitise():
            return False, "INVALID_ARGUMENTS"

        triggered, error = CPUHandler.check_loadavg(operation=self.operation, thresholds=self.threshold)
        return self.eval_negate(triggered, error)

    def sanitise(self):

        """
            **Method to check validity of the params**

            Returns:
                bool : params are proper or not
        """
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

        if not self.check:

            '''
                Log error
            '''
            return False

        if not self.check in self.valid_checks:

            '''
                Log error
            '''
            return False

        for val in self.threshold:
            if val != "-" and type(val) != float:

                '''
                    Log error
                '''
                return False

        return True
