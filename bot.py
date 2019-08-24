from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler # Extended Telegram API
import logging
import telegram
from telegram.chataction import ChatAction # pure Telegram API (send_message method) #REVIEW 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
import requests #3rd party module
import scrape
from configFile import * #REVIEW 
import time


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
        context.bot.send_message(chat_id=update.message.chat_id, text="Hey!, I'll record your chatId. Please provide the amazon link.")

    def addProduct(self, update, context):
        print("Enter: addProduct")
        """ Add product to tracking for the user """
        context.bot.send_message(chat_id=update.message.chat_id, text="Adding product to tracking... Please wait")
        print(''.join(context.args))
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
        # FIXME Time out not working on /addhttps://amazon.in type links
        response = requests.get(''.join(context.args), headers=headers, timeout=5)
        print(response.status_code)
        print(type(response.status_code))
        print("Before: respone.status_code")
        if response.status_code == 200:
            # add product to tracking list
            addProduct = scrape.UpdateTrackingList(''.join(context.args), update.message.chat_id)
            if addProduct.addToTrackingList():
                print("Bot: After if addToTrackingList")
                context.bot.send_message(chat_id=update.message.chat_id, text="I've added your product for tracking. Now use /alert <price> to set alert price.")
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="Only one product per user allowed.")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Invalid URL!")

    def setAlertValue(self, update, context):
        """ Set price threshold for the user """
        print("Enter: setAlertValue")
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        updateAlert = scrape.ChangeAlert(update.message.chat_id, ''.join(context.args))
        if updateAlert.changeAlert():
                print("Bot: After if chageAlert")
                context.bot.send_message(chat_id=update.message.chat_id, text="Price updated to {},".format(''.join(context.args)))
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="You must add a product first.")



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
        # watch the requests
        #NOTE Create thread of watch
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

