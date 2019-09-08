import json

class ParseJson():
    """ Parse config data from config.json file """
    def __init__(self, jsonFile="config.json"):
        self.jsonFile = jsonFile

    def getConfig(self):
        with open(self.jsonFile, "r", encoding="utf-8") as configFile:
            config = json.load(configFile)
        return config['botToken']
