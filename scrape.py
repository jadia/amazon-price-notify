import requests # request product page from amazon.in
from bs4 import BeautifulSoup # parsing the page
from re import sub # substitute , in currency
from decimal import Decimal # better currency representation
import time
from datetime import datetime # logging #REVIEW 
import bot 
import threading 
import logging
import parseConfig

# format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=format, level=INFO,
#                     datefmt="%H:%M:%S")

# Global var to track user and it's product data
PRODUCTLIST = dict()
killThread = ""

class ScrapeAmazon():
    """ Scrape amazon product page and decide on sending telegram notification """

    def __init__(self, productDetails):
        print("Enter: ScrapeAmazon class")
        self.productDetails = productDetails
        print(self.productDetails.chatId)
        print(self.productDetails.productURL)
        print(self.productDetails.threshold)
        print(self.productDetails.epoch)
        # botToken used in getWebPage()
        getToken = parseConfig.ParseJson()
        self.botToken = getToken.getConfig()
        print(self.botToken)

    def convertCurrency(self, price):
        """ Convert extracted price to decimal type value """
        print("Enter: convertCurrency")
        # remove whatever is not a digit or . and return Decimal type value 
        return Decimal(sub(r'[^\d.]','', price))

    def comparePrices(self, currentPrice, thresholdPrice):
        """ Compare current price with the threashold price set by user """
        print("Enter: comparePrices")
        if currentPrice <= thresholdPrice:
            return True
        else:
            return False

    def getWebPage(self):
        """ Get HTML page using requests and Beautifulsoup """
        # Cool down time (sec) on price drop notification
        coolDownTime = 10800 # 3hrs

        print("Enter: getWebPage")
        # Without a proper User-Agent Amazon will block the request
        # TODO  Randomize the User-Agen to escape IP ban.
        headers = {
        #"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36' }
        htmlPage = requests.get(self.productDetails.productURL, headers = headers)
        # Use beautifulSoup to parse the page
        soup1 = BeautifulSoup(htmlPage.content,'html.parser')
        # second soup because amazon uses javascript to create the price
        soup2 = BeautifulSoup(soup1.prettify(),'html.parser')
        # get product title
        productTitle = soup2.find('span', id='productTitle').getText()
        print(productTitle.strip())
        # get product price
        productPriceStr = soup2.find('span', id='priceblock_ourprice').getText()
        print(productPriceStr.strip())
        productPrice = self.convertCurrency(productPriceStr.strip())
        # register price and title in object
        self.productDetails.productTitle = productTitle
        self.productDetails.productPrice = productPrice
        # print product and price
        # NOTE This will be modified into log file
        now = datetime.now()
        print("\n", now)
        print(productPrice)

        if self.comparePrices(productPrice, Decimal(self.productDetails.threshold)):
            notify = bot.TelegramNotification(self.botToken, self.productDetails.chatId)
            notify.sendNotification(productTitle, productPriceStr)
            print("Stop notification for 6 hours")
            self.productDetails.epoch = self.productDetails.epoch + coolDownTime
        else:
            print(now, "Price still higher.")

    def startTracking(self):
        # Scrape product page after every scrapeInterval time
        scrapeInterval = 900 # 15min
        print("Enter: startTracking")
        global killThread
        ## TODO  Catch except and send notification about no more tracking
        while True:
            if killThread == self.productDetails.chatId:
                print("Killing Thread due to new product.")
                killThread = ""
                print(f"Done resetting killThread var to {killThread}")
                exit()
            else:
                if self.productDetails.epoch < time.time():
                    print(f"{self.productDetails.epoch} < {time.time()}")
                    self.getWebPage()
                    self.productDetails.epoch = self.productDetails.epoch + scrapeInterval



class ProductInfo():
    """ Manage product information """

    def __init__(self, productURL, chatId):
        print("Enter: ProductInfo class")
        self.productURL = productURL
        self.chatId = chatId
        self.epoch = time.time()
        self.threshold = -1 #Min value
        self.productTitle = ""
        self.productPrice = -1
    
    
class ChangeAlert():
    """ Change alert value"""

    def __init__(self, chatId, newThreshold):
        self.chatId = chatId
        self.newThreshold = newThreshold.strip()

    def priceTypeCheck(self):
        print("Enter: priceTypeCheck")
        if self.newThreshold.isdigit():
            return True
        else:
            return False

    def changeAlert(self):
        """ Change alert value """
        ## TODO  Check if user exists.
        if self.chatId in PRODUCTLIST:
            print("Updating price")
            print("Current Price")
            print(PRODUCTLIST.get(self.chatId).threshold)
            PRODUCTLIST.get(self.chatId).threshold = self.newThreshold
            print("New Price")
            print(PRODUCTLIST.get(self.chatId).threshold)
            print("Success to changeAlert")
            return True
        else:
            print("User did not add product let")
            return False

class UpdateTrackingList():
    """ Update the changes in tracking list """
    def __init__(self, productURL, chatId):
        print("Enter: UpdateTrackingList class")
        self.productDetails = ProductInfo(productURL, chatId)

    def addToTrackingList(self):
        print("Enter: Add to tracking list")
        # create a new object for the product and append it to the list
        # create a thread for live tracking
        global killThread
        replaceProduct = False
        #FIXME  Do not allow multiple products to single user.
        # Check if user already has the product
        if self.productDetails.chatId in PRODUCTLIST:
            # kill the old thread before starting the new one
            killThread = self.productDetails.chatId
            replaceProduct = True
            time.sleep(2) # let the old thread die
        startScraping = ScrapeAmazon(self.productDetails)
        x = threading.Thread(target=startScraping.startTracking, name=self.productDetails.chatId)
        x.daemon=True
        PRODUCTLIST[self.productDetails.chatId] = self.productDetails
        print("Before: Thread starts ")
        x.start()
        if replaceProduct:
            # False will say "Notify user that old product link is replaced"
            # This has nothing to do with True or False
            return False
        return True
