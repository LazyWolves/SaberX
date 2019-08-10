from .triggerbase import TriggerBase
from .filehandler import FileHandler

class FileTrigger(TriggerBase):
	def __init__(self, **kwargs):
		super(FileTrigger, self).__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("regex"):
			self.regex = kwargs.get("regex")
		if kwargs.get("position"):
			self.position = kwargs.get("position")
		if kwargs.get("limit"):
			self.limit = kwargs.get("limit")
		if kwargs.get("resource"):
			self.path = kwargs.get("resource")

		self.valid_checks = ["empty", "present", "regex"]
		self.valid_positions = ["head", "tail"]

	def fire_trigger(self):
		if not self.sanitise():
			return False, "IMPROPER_ARGUMENTS"

		if self.check == "present":
			triggered, error =  FileHandler.is_present(self.path)
			return self.eval_negate(triggered, error)

		if self.check == "empty":
			triggered, error =  FileHandler.is_empty(self.path)
			return self.eval_negate(triggered, error)

		if self.check == "regex":
			triggered, error = FileHandler.search_keyword(path=self.path, limit=self.limit, position=self.position, regex=self.regex)
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
