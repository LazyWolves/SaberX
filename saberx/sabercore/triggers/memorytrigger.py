from .triggerbase import TriggerBase
from .memoryhandler import MemoryHandler

class MemoryTrigger(TriggerBase):
	def __init__(self, **kwargs):
		super(MemoryTrigger, self).__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("attr"):
			self.attr = kwargs.get("attr")
		if kwargs.get("operation"):
			self.operation = kwargs.get("operation")
		if kwargs.get("threshold"):
			self.threshold = kwargs.get("threshold")

		self.valid_checks = ["virtual", "swap"]
		self.valid_attrs = ["used", "available", "free"]
		self.valid_operations = ["=", "<", ">", "<=", ">="]

	def fire_trigger(self):
		if not self.sanitise():
			return False, "INVALID_ARGUMENTS"

		triggered, error = MemoryHandler.check_mem(check_type=self.check, attr=self.attr, operation=self.operation, threshold=self.threshold)
		return self.eval_negate(triggered, error)

	def sanitise(self):
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

		if not self.check in self.valid_checks:

			'''
				Log error
			'''
			return False

		if not self.attr:

			'''
				Log error
			'''
			return False

		if not self.attr in self.valid_attrs:

			'''
				Log error
			'''
			return False

		if not self.operation:

			'''
				Log error
			'''
			return False

		if not self.operation in self.valid_operations:

			'''
				Log error
			'''
			return False

		if not self.threshold:

			'''
				Log error
			'''

			return False

		if type(self.threshold) != float:

			'''
				Log error
			'''

			return False
