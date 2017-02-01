import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import praw, obot
import random

print("Setting up Config")

''' PRAW CONFIG '''

WAIT = 15
ERROR_WAIT = 20
MAXPOSTS = 100

''' SETUP COMPLETED'''

print('Logging into Reddit')

r = obot.login()

print('Login succesful')



bot = telegram.Bot(token="304300939:AAGOQCXUuA4laeKEZkJuwppQaE-kosTGzxQ")
updater = Updater(token = '304300939:AAGOQCXUuA4laeKEZkJuwppQaE-kosTGzxQ')
dispatcher = updater.dispatcher

def parse_reddit(SUBREDDIT):
    global URL_LIST
    s = r.get_subreddit(SUBREDDIT)
    URL_LIST = []
    for submission in s.get_top(limit=25):
        URL = submission.url
        URL_LIST.append(URL)
    return URL_LIST

def Current_Subreddit(bot, update):
    print(URL_LIST)
    bot.sendMessage(chat_id=update.message.chat_id, text='''Status:
    {}
    '''.format(SUBREDDIT))

def Send_Photo(bot, update):
    REDDIT_URLS = parse_reddit(SUBREDDIT)
    file = random.choice(REDDIT_URLS)
    print(file)
    if ".gifv" in file or "gfycat" in file:
        print("Ich will ein Gif schicken")
        bot.sendDocument(chat_id=update.message.chat_id, document=file)
    else:
        print("Ich will ein Foto schicken")
        bot.sendPhoto(chat_id=update.message.chat_id, photo=file)

def Available_Subreddits(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text= '''
You can set any Subreddit you want, just make sure it actually has images on it.
You can set a subreddit by doing the following:

/setsubreddit memes

Change memes for whatever subreddit you would like to set.
After that just use /getImage to post a Image off Reddit''')

def Set_Subreddit(bot, update, args):
    global SUBREDDIT
    for chosensubreddit in args:
        SUBREDDIT = chosensubreddit
        print(SUBREDDIT)
        URL_LIST = []
    bot.sendMessage(chat_id=update.message.chat_id, text= "Subreddit set to {}!".format(chosensubreddit))
    return SUBREDDIT, URL_LIST

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='''
To start using me, use the command /HowTo

Available commands:
/start
/howto
/currentsubreddit
/getimage
/setsubreddit''')


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('currentsubreddit', Current_Subreddit))
updater.dispatcher.add_handler(CommandHandler('getimage', Send_Photo))
updater.dispatcher.add_handler(CommandHandler('howto', Available_Subreddits))
updater.dispatcher.add_handler(CommandHandler('setsubreddit', Set_Subreddit, pass_args = True))

updater.start_polling()
