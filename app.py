#!/usr/bin/python3

"""app.py: Primitive webscarping script"""

__author__ = "Nitish Jadia"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "nitish@jadia.dev"
__status__ = "Development"

import requests #3rd party module
from bs4 import BeautifulSoup # parsing the page
from re import sub # substitute , in currency
from decimal import Decimal # better currency representation
import telegram # send telegram notification

def convertCurrency(price):
    return Decimal(sub(r'[^\d.]','', price))

def sendNotification(productTitle, productPrice):
    print("Notification to Telegram")
    bot = telegram.Bot(token="99292267:AAEW7E1QQFJWmzsMvYGtq5K3c60otrr2a4U")
    chat_id=74651551
    bot.send_message(chat_id=chat_id, text="PRICE REDUCED"+productTitle+productPrice)

def comparePrices(currentPrice, thresholdPrice):
    if currentPrice <= thresholdPrice:
        return True
    else:
        return False

def getWebPage(URL, threshold):
    # Get HTML page
    # Without a proper User-Agent Amazon will block the request
    headers = {
       "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
    htmlPage = requests.get(URL, headers = headers)
    # Use beautifulSoup to parse the page
    soup1 = BeautifulSoup(htmlPage.content,'html.parser')
    # second soup because amazon uses javascript to create the price
    soup2 = BeautifulSoup(soup1.prettify(),'html.parser')
    # get product title
    productTitle = soup2.find('span', id='productTitle').getText()
    # get product price
    productPriceStr = soup2.find('span', id='priceblock_ourprice').getText()
    productPrice = convertCurrency(productPriceStr.strip())
    # print product and price
    # NOTE This will be modified into log file
    print(productTitle.strip())
    print(productPrice)

    if comparePrices(productPrice, Decimal(threshold)):
        sendNotification(productTitle, productPriceStr)
    else:
        print("Price still higher.")

# Main
URL = "https://www.amazon.in/Passport-Portable-External-Hard-Drive/dp/B01LQQH85G"
#URL = "https://www.amazon.in/dp/B01GGKYJG8"
threshold = "9000"
# NOTE Take website links and add them to the list
getWebPage(URL, threshold)