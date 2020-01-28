"""
.. module:: tcptrigger
   :synopsis: Module for firing tcp trigger.
"""

from .triggerbase import TriggerBase
from .tcphandler import TCPHandler


class TCPTrigger(TriggerBase):

    """
        **Method for initialing memory trigger**

    """
    def __init__(self, **kwargs):
        super(TCPTrigger, self).__init__(
            type=kwargs.get("type"), 
            check=kwargs.get("check"), 
            negate=kwargs.get("negate"))

        self.host = kwargs.get("host", "127.0.0.1")
        self.port = kwargs.get("port", 80)
        self.attempts = kwargs.get("attempts", 3)
        self.threshold = kwargs.get("threshold", 1)
        self.timeout = kwargs.get("timeout", 5)
        self.ssl = kwargs.get("ssl", False)

        self.valid_checks = ["tcp_connect", "tcp_fail"]

        self.PORT_MIN, self.PORT_MAX = 0, 65535

    def fire_trigger(self):

        """
            **Method to fire the trigger**

            This method first sanitises the parameters, calls tcp handler
            to evaluate the trigger conditions and returns trigger status

            Returns:
                bool : Trigger fired or not
        """
        if not self.sanitise():
            return False, "IMPROPER_ARGUMENTS"

        trigerred, error = TCPHandler.check_connection(
            host=self.host, 
            port=self.port, 
            timeout=self.timeout, 
            attempts=self.attempts, 
            threshold=self.threshold, 
            check_type=self.check, 
            ssl=self.ssl)

        return self.eval_negate(trigerred, error)

    def sanitise(self):

        """
            **Method to check validity of the params**

            Returns:
                bool : params are proper or not
        """
        if not self.host:

            '''
                Log error
            '''
            return False

        if self.port < self.PORT_MIN or self.port > self.PORT_MAX:

            '''
                Log error
            '''
            return False

        if self.timeout <= 0:

            '''
                Log error
            '''
            return False

        if self.attempts <= 0:

            '''
                Log error
            '''
            return False

        if self.threshold <= 0:

            '''
                Log error
            '''
            return False

        if self.check not in self.valid_checks:

            '''
                Log error
            '''
            return False

        return True
