from triggerbase import TriggerBase
from filehandler import filehandler

class FileTrigger(TriggerBase):
	def __init__(self, **kwargs):
		TriggerBase.__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("regex"):
			self.regex = kwargs.get("regex")
		if kwargs.get("position"):
			self.position = kwargs.get("position")
		if kwargs.get("limit"):
			self.limit = kwargs.get("limit")

		self.checks = ["empty", "present", "regex"]
		self.valid_positions = ["head", "tail"]

	def fire_trigger(self):
		pass

	def sanitise(self):
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

		if not self.check in self.checks:
			'''
				Log error
			'''
			return False

		if self.limit and self.limit <= 0:
			'''
				Log error
			'''
			return False

		if self.position and not self.position in self.valid_positions:
			'''
				Log error
			'''
			return False
