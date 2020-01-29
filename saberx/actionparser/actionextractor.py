import yaml


class ActionExtractor:

    def __init__(self, **kwargs):
        self.configpath = kwargs.get("configpath")
        self.logger = kwargs.get("logger")
        self.action_plan_loaded = self.__load_config()

    def __load_config(self):
        with open(self.configpath) as config:
            try:
                self.config = yaml.load(config)
                self.__extract_action_groups()
                return True
            except Exception as e:

                '''
                    Log issue
                '''

                self.logger.critical(
                    "Failed to parse YAML : Exception : {}".format(str(e)))
                return False

    def __extract_action_groups(self):
        self.action_groups = self.config.get("actiongroups")

    def get_action_groups(self):
        return self.action_groups


if __name__ == "__main__":
    ActionExtractor(configpath="test.yaml")
