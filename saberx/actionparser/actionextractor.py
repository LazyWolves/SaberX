import yaml
import json

class ActionExtractor:

	def __init__(self, **kwargs):
		self.configpath = kwargs.get("configpath")
		self.__load_config()
		self.__action_plan_loaded = False
		print (json.dumps(self.config, indent=4))

	def __load_config(self):
		with open(self.configpath) as config:
			try:
				self.config = yaml.load(config)
				self.__action_plan_loaded = True
				self.__extract_action_groups()
			except Exception as e:

				'''
					Log issue
				'''
				pass

	def __extract_action_groups(self):
		self.action_groups = self.config.get("action_groups")

	def get_action_groups(self):
		return self.action_groups

	def action_plan_loaded(self):
		return self.__action_plan_loaded

if __name__ == "__main__":
	ActionExtractor(configpath="test.yaml")
