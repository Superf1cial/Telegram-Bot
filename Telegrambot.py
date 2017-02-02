import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import praw, obot
import random

print("Setting up Logging")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print("Setting up Config")

''' PRAW CONFIG '''

WAIT = 15
ERROR_WAIT = 20
MAXPOSTS = 100
SUBREDDIT = ""

''' SETUP COMPLETED'''

print('Logging into Reddit')

r = obot.login()

print('Login succesful')



bot = telegram.Bot(token="Your Api token")
updater = Updater(token ="Your Api token")
dispatcher = updater.dispatcher

def parse_reddit(SUBREDDIT):
    global URL_LIST
    global title_list
    s = r.get_subreddit(SUBREDDIT)
    URL_LIST = []
    title_list = []
    for submission in s.get_top(limit=50):
        URL = submission.url
        title = submission.title
        title_list.append(title)
        URL_LIST.append(URL)
        reddit_dict = dict(zip(title_list, URL_LIST))
    return reddit_dict

def Current_Subreddit(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="The current selected subreddit is: {}".format(SUBREDDIT))

def Send_Photo(bot, update):
    REDDIT_URLS = parse_reddit(SUBREDDIT)
    title, url = random.choice(list(REDDIT_URLS.items()))
    if ".gifv" in url:
        gif = url.replace(".gifv", ".mp4")
        bot.sendDocument(chat_id=update.message.chat_id, document=gif)
        bot.sendMessage(chat_id=update.message.chat_id, text=title)
    elif "gfycat" in url:
        bot.sendMessage(chat_id=update.message.chat_id, text="Currently unable to send Gfycat links, I'm working on it.")
    else:
        bot.sendPhoto(chat_id=update.message.chat_id, photo=url)
        bot.sendMessage(chat_id=update.message.chat_id, text=title)

def Set_Subreddit(bot, update, args):
    global SUBREDDIT
    for chosensubreddit in args:
        SUBREDDIT = chosensubreddit
        print(SUBREDDIT)
        URL_LIST = []
    bot.sendMessage(chat_id=update.message.chat_id, text= "Subreddit set to {}!".format(chosensubreddit))
    return SUBREDDIT, URL_LIST

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="To start set a subreddit. /setsubreddit name. After that use /getimage for a picture or gif")

def getjoke(bot, update):
    title = []
    text = []
    s = r.get_subreddit("jokes")
    for submission in s.get_top(limit=50):
        title.append(submission.title)
        text.append(submission.selftext)
        reddit_dict = dict(zip(title, text))
    headline, story = random.choice(list(reddit_dict.items()))
    bot.sendMessage(chat_id=update.message.chat_id, text=headline)
    bot.sendMessage(chat_id=update.message.chat_id, text=story)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('currentsubreddit', Current_Subreddit))
updater.dispatcher.add_handler(CommandHandler('getimage', Send_Photo))
updater.dispatcher.add_handler(CommandHandler('setsubreddit', Set_Subreddit, pass_args = True))
updater.dispatcher.add_handler(CommandHandler('getjoke', getjoke))

updater.start_polling()
