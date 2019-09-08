# Amazon Price drop notification script

A Python application to monitor an Amazon.in product and send notification through telegram on price drop.

The application has two parts:

1. Monitor price
2. Send notification

**Monitor price:**

Requests and Beautifulsoup modules are used to scrape the page and get the product title and it's price. The product page is scrapped every 15 min.

**Send notification:**

Generate a price drop alert to user via Telegram API using `python-telegram-bot` module.

Once price drop notification is sent to the user, to avoid bothering the user, it snoozes notifications for next 3hrs.

## Installation

### Install on Local machine

Install dependencies (debian/ubuntu):

```bash
sudo apt-get -y install python3-pip && \
sudo pip3 install -r requirements.txt
```

The script was tested on Python 3.7.3.

Refer official telegram documentaion on [How to create a new bot](https://core.telegram.org/bots#creating-a-new-bot)

Put the `botToken` generated from @botFather in `config.json` and run `main.py`.

```bash
python3 ./main.py
```

**botToken:** Token given by botFather when new bot is created. 

### Set-up on Heroku

Create an account on Heroku and install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

```bash
curl https://cli-assets.heroku.com/install.sh | sudo sh
```

Login into Heroku

```bash
sudo heroku login
```

Goto heroku website and create a `new app`. Note down the name of application when you create it. It will be used in below commands.

Clone this repository

```bash
git clone https://github.com/th3nyx/amazon-price-notify.git && \
cd amazon-price-notify && \
heroku git:remote -a YOUR-HEROKU-APPLICATION-NAME
```

Deploy your application and watch logs:

```bash
sudo git add . && \
sudo git commit -am "make it better" && \
sudo git push heroku master && \
heroku logs --tail
```

**NOTE:** Heroku free account kills the container after half an hour. Add your heroku application to [UptimeRobot](https://uptimerobot.com/) to keep it alive.  

As of 2019-08-26: Heroku only allows 550hrs/month for free accounts without credit card verification.

## Usage

![telegram bot screenshot](/docs/resources/telegram-ss.png)

Search for your bot on telegram and start conversation.

**/start:** Bot sends you an introduction  
**/add:** Add your product  
**/alert:** Create alert  

## Demo

Visit [amazon-price-tracker-bot.herokuapp.com](https://amazon-price-tracker-bot.herokuapp.com/) to spin up the heroku application if it's dead.  
Search for `testbot13371` on Telegram and start the conversation.

**Note:** *The test bot should work if Amazon.in haven't changed their HTML tags*

## To-do

- [x] Use classes and object to support multiple products later.
- [x] Use Threads to track multiple items on watch.
- [x] Enable user to provide link directly from telegram app.
- [x] Accept all kinds to URL
- [x] Type checking of input data.
- [x] Heroku integration.
- [x] Overwrite old product when new product is added
- [x] Add cooldown timer once notification is sent. (6hrs timer)
- [ ] Add snooze command to stop notifications for that many hours.
- [ ] Randomize User-Agent to avoid IP ban from Amazon.
- [ ] Exception handeling.
- [ ] Move timers value to config file
- [ ] Introduce database to stop the links, so server restart or script crash won't affect the links.
- [ ] Deploy on AWS
**Future Work:**

- [ ] Create a telegram menu and inlineKeyboard to replace commands.
- [ ] Support for multiple products per customer.

## Known-Issues

1. If price of product is below threshold for more than 15 min. There will be multiple notifications.
2. ~~Incorrect URL hangs the application.~~ (FIXED)
