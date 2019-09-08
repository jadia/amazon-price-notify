#!/usr/bin/python3

"""app.py: Primitive webscraping script"""

__author__ = "Nitish Jadia"
__license__ = "MIT"
__version__ = "0.2"
__email__ = "nitish@jadia.dev"
__status__ = "Development"


import time # sleep # epoch time 
import scrape # scrape amazon page
import bot # poweron telegram bot + heroku support
import parseConfig # read config.json file

if __name__ == '__main__':
    """ Get token from config.json and initialize the bot """
    getToken = parseConfig.ParseJson()
    botToken = getToken.getConfig()
    theBot = bot.RespondToCommands(botToken)
    theBot.initializeBot()

