import requests
from   bs4 import BeautifulSoup
import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


links_text = {}

print("Starting up Telegram bot API")

bot = telegram.Bot(token="304300939:AAGOQCXUuA4laeKEZkJuwppQaE-kosTGzxQ")
updater = Updater(token = '304300939:AAGOQCXUuA4laeKEZkJuwppQaE-kosTGzxQ')
dispatcher = updater.dispatcher

print("Parsing data from mydealz")

url = 'https://www.mydealz.de/'
raw = requests.get(url)
soup = BeautifulSoup(raw.text, 'html.parser')

print("Generating dictionary")

for a in soup.find_all("a", {"class": "cept-tt thread-link linkPlain space--r-1 space--v-1"}):
    text = a.get_text()
    link = (str(a['href']))
    links_text.update({text : link})

for key, value in links_text.items():
    bot.sendMessage(chat_id="327675553", text=key)
    bot.sendMessage(chat_id="327675553", text=value)

updater.start_polling()
