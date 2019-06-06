class TriggerBase:
	def __init__(self, **kwargs):
		self.type = kwargs.get("type")
		self.check = kwargs.get("check")
		self.nagate = kwargs.get("negate", False)

	def fire_trigger(self):
		'''
			This method must be implemented by child class
		'''

		return False, None

	def get_type(self):
		return type

	def get_check(self):
		return check

	def is_negate(self):
		return negate
