#!/usr/bin/python3

"""app.py: Primitive webscarping script"""

__author__ = "Nitish Jadia"
__license__ = "MIT"
__version__ = "0.2"
__email__ = "nitish@jadia.dev"
__status__ = "Development"

import requests #3rd party module
from bs4 import BeautifulSoup # parsing the page
from re import sub # substitute , in currency
from decimal import Decimal # better currency representation
import telegram # send telegram notification
import time
from datetime import datetime
from configFile import *



class telegramNotification():
    def __init__(self, botToken, chatId):
        self.botToken = botToken
        self.chatId = chatId

    def sendNotification(self, productTitle, productPrice):
        print("Notification to Telegram")
        bot = telegram.Bot(token=self.botToken)
        bot.send_message(chat_id=self.chatId, text="PRICE REDUCED"+" \n"+productTitle.strip()+" \n"+productPrice.strip()+" \n \n")


class scrapeAmazon(telegramNotification):
    def __init__(self, URL, threshold, botToken, chatId):
        self.URL = URL
        self.threshold = threshold
        self.botToken = botToken
        self.chatId = chatId

    def convertCurrency(self, price):
        # remove whatever is not a digit or . and return Decimal type value 
        return Decimal(sub(r'[^\d.]','', price))

    def comparePrices(self, currentPrice, thresholdPrice):
        if currentPrice <= thresholdPrice:
            return True
        else:
            return False

    def getWebPage(self):
        # Get HTML page
        # Without a proper User-Agent Amazon will block the request
        # TODO  Randomize the User-Agen to escape IP ban.
        headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
        htmlPage = requests.get(self.URL, headers = headers)
        # Use beautifulSoup to parse the page
        soup1 = BeautifulSoup(htmlPage.content,'html.parser')
        # second soup because amazon uses javascript to create the price
        soup2 = BeautifulSoup(soup1.prettify(),'html.parser')
        # get product title
        productTitle = soup2.find('span', id='productTitle').getText()
        # get product price
        productPriceStr = soup2.find('span', id='priceblock_ourprice').getText()
        productPrice = self.convertCurrency(productPriceStr.strip())
        # print product and price
        # NOTE This will be modified into log file
        now = datetime.now()
        print("\n", now)
        print(productTitle.strip())
        print(productPrice)

        if self.comparePrices(productPrice, Decimal(self.threshold)):
            notify = telegramNotification(self.botToken, self.chatId)
            notify.sendNotification(productTitle, productPriceStr)
        else:
            print(now, "Price still higher.")
    
    def startPriceCheck(self):
        pass

# Main
# For the time being URL and threshold are being hard coded
# NOTE Take website links and add them to the list
start = scrapeAmazon(URL, threshold, botToken, chatId)
#start.getWebPage()
while True:
    start.getWebPage()
    time.sleep(900) # 15 minutes