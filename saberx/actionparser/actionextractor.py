import yaml
import json

class ActionExtractor:

	def __init__(self, **kwargs):
		self.configpath = kwargs.get("configpath")
		self.__load_config()
		self.action_plan_loaded = False
		print (json.dumps(self.config, indent=4))

	def __load_config(self):
		with open(self.configpath) as config:
			try:
				self.config = yaml.load(config)
				self.action_plan_loaded = true
				self.__extract_action_groups()
				self.action_plan_loaded = True
			except Exception as e:

				'''
					Log issue
				'''
				pass

	def __extract_action_groups(self):
		self.action_groups = self.config.get("action_groups")

	def get_action_groups(self):
		return self.action_groups

if __name__ == "__main__":
	ActionExtractor(configpath="test.yaml")
