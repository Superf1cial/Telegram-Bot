import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import praw, obot
import random

print("Setting up Config")

''' PRAW CONFIG '''

WAIT = 15
ERROR_WAIT = 20
MAXPOSTS = 100
URL_LIST = []
SUBREDDIT = "memes"

''' SETUP COMPLETED'''

print('Logging into Reddit')

r = obot.login()

print('Login succesful')



bot = telegram.Bot(token="304300939:AAGOQCXUuA4laeKEZkJuwppQaE-kosTGzxQ")
updater = Updater(token = '304300939:AAGOQCXUuA4laeKEZkJuwppQaE-kosTGzxQ')
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='''Available commands:
    
    /pic
    /subreddits
    /setsubreddit

    ''')

def Send_Photo(bot, update, SUBREDDIT):
    s = r.get_subreddit(SUBREDDIT)
    print(s)
    for submission in s.get_hot(limit=25):
        URL = submission.url
        URL_LIST.append(URL)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=random.choice(URL_LIST))

def Available_Subreddits(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text= '''
/r/memes
/r/funny
/r/pics
/r/funnypictures
/r/woahdude
/r/wallpapers
/r/techsupportgore''')

def Set_Subreddit(bot, update, args):
    for chosensubreddit in args:
        SUBREDDIT = chosensubreddit
        print(SUBREDDIT)
        URL_LIST = []
    bot.sendMessage(chat_id=update.message.chat_id, text= "Subreddit set to {}".format(chosensubreddit))
    return SUBREDDIT

updater.dispatcher.add_handler(CommandHandler('status', start))
updater.dispatcher.add_handler(CommandHandler('pic', Send_Photo))
updater.dispatcher.add_handler(CommandHandler('subreddits', Available_Subreddits))
updater.dispatcher.add_handler(CommandHandler('setsubreddit', Set_Subreddit, pass_args = True))

updater.start_polling()
