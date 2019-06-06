from triggerbase import TriggerBase

class FileTrigger(TriggerBase):
	def __init__(self, **kwargs):
		TriggerBase.__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("regex"):
			self.regex = kwargs.get("regex")
		if kwargs.get("position"):
			self.position = kwargs.get("position")
		if kwargs.get("limit"):
			self.limit = kwargs.get("limit")

	def fire_trigger(self):
		pass
