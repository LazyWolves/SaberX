import yaml

class ActionExtractor:

	def __init__(self, **kwargs):
		self.configpath = kwargs.get("configpath")
		self.__load_config()
		self.__extract_actions()

	def __load_config():
		with open(self.configpath) as config:
			self.config = yaml.load(config)

	def __extract_actions():
		pass
