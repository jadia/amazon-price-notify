#!/usr/bin/python3

"""app.py: Primitive webscraping script"""

__author__ = "Nitish Jadia"
__license__ = "MIT"
__version__ = "0.2"
__email__ = "nitish@jadia.dev"
__status__ = "Development"


import time # sleep # epoch time 
#from configFile import * #REVIEW 
import scrape
import bot
import parseConfig

if __name__ == '__main__':
    getToken = parseConfig.ParseJson()
    botToken = getToken.getConfig()
    theBot = bot.RespondToCommands(botToken)
    theBot.initializeBot()

