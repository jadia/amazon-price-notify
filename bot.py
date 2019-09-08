from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler # Extended Telegram API
import logging
import telegram
from telegram.chataction import ChatAction # pure Telegram API (send_message method) #REVIEW 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
import requests #3rd party module
import scrape
import time
import re


# format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=format, level=logging.DEBUG,
#                     datefmt="%H:%M:%S")

class RespondToCommands():
    """ Class to initialize the telegram dispacher and respond to the commands """

    def __init__(self, botToken):
        self.botToken = botToken

    #update.message.text
    def unknown(self, update, context):
        print("Enter: Unknown")
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I cannot understand that command.")

    def start(self, update, context):
        print("Enter: Start")
        context.bot.send_message(chat_id=update.message.chat_id, text="Hey! \nWelcome to Amazon Price Tracker bot. \nStart with adding your product:\n /add <amazon URL> \n\nSet price alert for your product:\n /alert <price> \n\n Only one product can be tracked per user. ")

    def preprocessURL(self, productURL):
        """ Validate and clean the amazon.in URL """
        # remove everything after ?ref= , /ref= or a ? and return a valid URL else False
        print("Enter: preProcessURL")
        amazonURL = re.match(r'^(https://|http://)(www.)*amazon.in/[a-zA-Z0-9-]*[/]*dp/[A-Z0-9]+[/?]?',productURL)
        if amazonURL:
            print(f"amazonURL:{amazonURL.group(0)}")
            print("preprocessURL: True")
            return True, amazonURL.group(0)
        else:
            print("preprocessURL: False")
            return False, ""



    def addProduct(self, update, context):
        """ Add product to tracking for the user """
        print("Enter: addProduct")
        # TODO Add typing decoration
        context.bot.send_message(chat_id=update.message.chat_id, text="Adding product to tracking... Please wait")
        # addArgs arguments passed with /add command. Expected to be amazon url
        addArgs = ''.join(context.args)
        print(addArgs)
        headers = {
        #    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36' }
        isValid, validURL = self.preprocessURL(addArgs)
        if isValid:
            response = requests.get(validURL, headers=headers, timeout=5)
            print(response.status_code)
            print(type(response.status_code))
            print("Before: respone.status_code")
            if response.status_code == 200:
                # add product to tracking list
                addProduct = scrape.UpdateTrackingList(validURL, update.message.chat_id)
                if addProduct.addToTrackingList():
                    print("Bot: After if addToTrackingList")
                    context.bot.send_message(chat_id=update.message.chat_id, text="Great! Product is successfully added. Now set price alerts:\n\n /alert <price> ")
                else:
                    context.bot.send_message(chat_id=update.message.chat_id, text="Old product is replaced with the new one.")
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="Product URL unreachable. Try again later.")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Invalid arguments. Not a vaild Amazon.in URL.")



    def setAlertValue(self, update, context):
        """ Set price threshold for the user """
        print("Enter: setAlertValue")
        #context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        updateAlert = scrape.ChangeAlert(update.message.chat_id, ''.join(context.args))
        if updateAlert.priceTypeCheck():
            if updateAlert.changeAlert():
                    print("Bot: After if chageAlert")
                    context.bot.send_message(chat_id=update.message.chat_id, text="Price updated to {}".format(''.join(context.args)))
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="You must add a product first.")
        else:
                context.bot.send_message(chat_id=update.message.chat_id, text="Invalid price. Ex:\n /alert 8000")


    def caps(self, update, context):
        """ Reply with CAPS of args. Just for debugging """
        # text_caps = ' '.join(context.args)
        # print(text_caps)
        # print(len(text_caps))
        # context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

    def initializeBot(self):
        """ Initialize the bot """
        # creating updater and dispatcher
        updater = Updater(token=self.botToken, use_context=True)
        dispatcher = updater.dispatcher
        # create "start" command handler
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        # create "add" command handler
        addHandler = CommandHandler('add', self.addProduct)
        dispatcher.add_handler(addHandler)
        # create "alert" command handler
        alertHandler = CommandHandler('alert', self.setAlertValue)
        dispatcher.add_handler(alertHandler)
        # create "caps" command handler
        caps_handler = CommandHandler('caps', self.caps)
        dispatcher.add_handler(caps_handler)

        # *** unknown handler MUST be added at LAST ***
        # create "unknown" command handler
        unknown_handler = MessageHandler(Filters.text, self.unknown)
        dispatcher.add_handler(unknown_handler)

# FIXME  Create an easy way to switch heroku deployment on and off

        # Start the webhook
        # Change amazon-price-tracker-bot with your own heroku app name
        # Uncomment the below code to make it work with heroku.
        # also use uptimerobot service to keep the container alive
        # ***********************************
        # import os
        # PORT = os.environ.get('PORT')
        # updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=self.botToken)
        # updater.bot.setWebhook("https://{}.herokuapp.com/{}".format("amazon-price-tracker-bot", self.botToken))
        
        
        # watch the requests
        print("Starting: Updater Pool")
        updater.start_polling()


class TelegramNotification():
    """ Class to send telegram notification """
    def __init__(self, botToken, chatId):
        print("Enter: TelegramNotification class")
        self.botToken = botToken
        self.chatId = chatId

    def sendNotification(self, productTitle, productPrice):
        print("Enter: Notification to Telegram")
        bot = telegram.Bot(token=self.botToken)
        bot.send_message(chat_id=self.chatId, text="PRICE REDUCED"+" \n"+productTitle.strip()+" \n"+productPrice.strip()+" \n \n")

