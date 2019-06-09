from triggerbase import TriggerBase

class ProcessTrigger(TriggerBase):
	def __init__(self, **kwargs):
		TriggerBase.__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("regex"):
			self.regex = kwargs.get("regex")
		if kwargs.get("count"):
			self.count = kwargs.get("count")
		if kwargs.get("operation"):
			self.path = kwargs.get("operation")

		self.valid_checks = ["name", "cmdline"]
		self.valid_operations = ["=", "<", ">", "<=", ">="]

	def fire_trigger(self):
		if not self.sanitise():
			return False, "INVALID_ARGUMENTS"

		if self.check == "name":
			pass

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
