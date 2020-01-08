import requests
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler

def getLinks(data):
    links = []
    for entry in data:
        links.append([entry['name'], entry['forks_url']])
    return links

def getData(url):
	r = requests.get(url)
	return r.json()

data = getData('https://api.github.com/orgs/fedora-infra/repos')
links = getLinks(data)


def sendForks(update, context):
    args = "".join(context.args).strip()
    if args == "":
        for link in links:
            context.bot.send_message(chat_id=update.effective_chat.id, text=link[1])
    else:
        # These are the links by that particular person
        sub_links = []
        for link in links:
            if link[0] == args:
                sub_links.append(link[1])
        
        sub_links.insert(0, f'{args} has {len(sub_links)} repos. They are: ')
        sub_links = "\n".join(sub_links)
        context.bot.send_message(chat_id=update.effective_chat.id, text=sub_links)

updater = Updater(token='1056953929:AAGKVZpg4OR6NgQMeGesXl9u2nfjMRJMocc', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


start_handler = CommandHandler('forks', sendForks)
dispatcher.add_handler(start_handler)

updater.start_polling()