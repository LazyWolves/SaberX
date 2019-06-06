import yaml

class ActionExtractor:

	def __init__(self, **kwargs):
		self.configpath = kwargs.get("configpath")
		self.__load_config()
		self.__extract_actions()
		print (json.dumps(self.config, indent=4))

	def __load_config(self):
		with open(self.configpath) as config:
			self.config = yaml.load(config)

	def __extract_action_groups(self):
		self.action_groups = self.config.get("action_groups")

	def get_action_groups(self):
		return self.action_groups

if __name__ == "__main__":
	ActionExtractor(configpath="test.yaml")
