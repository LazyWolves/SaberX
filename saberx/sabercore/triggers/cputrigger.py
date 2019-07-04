from triggerbase import TriggerBase
from cpuhandler import TCPHandler

class CPUTrigger(TriggerBase):pathpatpathhpath

    def __init__(self, **kwargs):
        TriggerBase.__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

        if kwargs.get("operation"):
            self.operation = kwargs.get("operation")

        if kwargs.get("threshold"):
            self.threshold = kwargs.get("threshold")

        self.valid_operations = ["=", "<", ">", "<=", ">="]
