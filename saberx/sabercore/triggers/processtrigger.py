from .triggerbase import TriggerBase
from .processhandler import ProcessHandler

class ProcessTrigger(TriggerBase):
	def __init__(self, **kwargs):
		super(ProcessTrigger, self).__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("regex"):
			self.regex = kwargs.get("regex")
		self.count = kwargs.get("count", 1)
		self.operation = kwargs.get("operation", "=")

		self.valid_checks = ["name", "cmdline"]
		self.valid_operations = ["=", "<", ">", "<=", ">="]

	def fire_trigger(self):
		if not self.sanitise():
			return False, "INVALID_ARGUMENTS"

		if self.check == "name":
			if self.count != None:
				triggered, error = ProcessHandler.check_name_count(self.regex, self.count, self.operation)
				return self.eval_negate(triggered, error)
			triggered, error = ProcessHandler.check_name(self.regex)
			return self.eval_negate(triggered, error)

		if self.check == "cmdline":
			if self.count:
				triggered, error = ProcessHandler.check_cmdline_count(self.regex, self.count, self.operation)
				return self.eval_negate(triggered, error)
			triggered, error = ProcessHandler.check_cmdline(self.regex)
			return self.eval_negate(triggered, error)

	def sanitise(self):
		if not self.type:
			'''
				log error
			'''

			return False

		if not self.check:
			'''
				log error
			'''

			return False

		if not (self.check in self.valid_checks):
			'''
				log error
			'''

			return False

		if self.count and self.count < 0:
			'''
				log error
			'''

			return False

		if self.count and not self.operation:
			'''
				log error
			'''

			return False

		if self.operation not in self.valid_operations:
			'''
				log error
			'''

			return False

		return True
