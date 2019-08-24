# Amazon Price drop notification script

## About

A Python script to monitor a product and send notification on telegram on price drop.

The application has two parts:

1. Monitor price
2. Send notification

### Monitor price

Requests and Beautifulsoup modules are used to scrape the page and get the product title and it's price. The product page is scrapped every 15 min.

### Send notification

Generate a price drop alert to user via Telegram API using `python-telegram-bot` module.

## Installation

The `requirements.txt` file contains the dependencies.

```bash
sudo pip3 install -r requirements.txt
```

The script was tested on Python 3.7.3.

## Using the application

Put required details in `configFile.py` and run `priceTracker.py`.

**botToken:** Token given by botFather when new bot is created.  
**chatId:** Get chatId of you and the bot by going the to [getUpdates endpoint](https://api.telegram.org/bot<botToken>/getUpdates)  
**threshold:** Minimum price value which will trigger the telegram notification.  

## Future-Work

- [x] Use classes and object to support multiple products later.
- [ ] Use Threads to track multiple items on watch.
- [ ] Enable user to provide link directly from telegram app.
- [ ] Introduce database to stop the links, so server restart or script crash won't affect the links.
- [ ] Randomize User-Agent to avoid IP ban from Amazon.
- [ ] Add cooldown timer once notification is sent.
- [ ] Create a telegram menu to select the product and remove it.

## Known-Issues

1. If price of product is below threshold for more than 15 min. There will be multiple notifications.
