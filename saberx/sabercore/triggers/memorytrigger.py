from triggerbase import TriggerBase
from memoryhandler import MemoryHandler

class MemoryTrigger(TriggerBase):
	def __init__(self, **kwargs):
		TriggerBase.__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("attr"):
			self.regex = kwargs.get("attr")
		if kwargs.get("operation"):
			self.operation = kwargs.get("operation")

		self.valid_checks = ["virtual", "swap"]
		self.valid_attrs = ["used", "available", "free"]
		self.valid_operations = ["=", "<", ">", "<=", ">="]

	def fire_trigger(self):
		pass

	def sanitise(self):
		pass