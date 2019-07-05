from triggerbase import TriggerBase
from cpuhandler import CPUHandler

class CPUTrigger(TriggerBase):

	def __init__(self, **kwargs):
		TriggerBase.__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("operation"):
			self.operation = kwargs.get("operation")

		if kwargs.get("threshold"):
			self.threshold = kwargs.get("threshold")

		self.valid_operations = ["=", "<", ">", "<=", ">="]
		self.valid_checks = ["loadavg"]

	def  fire_trigger(self):
		if not self.sanitise():
			return False, "INVALID_ARGUMENTS"

		triggered, error = CPUHandler.check_loadavg(operation=self.operation, thresholds=self.threshold)
		return self.eval_nagate(triggered, error)

	def sanitise(self):
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
