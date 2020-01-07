import requests
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler

def getLinks(data):
    links = []
    for a in data:
        for x in a.items():
            if x[0] == 'forks_url':
                links.append(x[1] + "\n")
    return links

def getData(url):
	r = requests.get(url)
	return r.json()

data = getData('https://api.github.com/orgs/fedora-infra/repos')
links = getLinks(data)


def sendLinks(update, context):
    for link in links:
        context.bot.send_message(chat_id=update.effective_chat.id, text=link)

updater = Updater(token='1056953929:AAGKVZpg4OR6NgQMeGesXl9u2nfjMRJMocc', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


start_handler = CommandHandler('Links', sendLinks)
dispatcher.add_handler(start_handler)

updater.start_polling()