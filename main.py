import requests
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler

def getLinks(data):
    links = []
    for entry in data:
        links.append([entry['name'], entry['forks_url'], entry['forks']])
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
        number = [link[2] for link in links if link[0] == args]
        
        toSend = f'{args} has {len(number)} repos.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=toSend)

def start(update, context):
    toSend = """Welcome, I'm AbtahaBot. Chat with me :).
Type /forks to get the list of all repos from fedora-infra
Type /forks name where name is the name of the contributer to get the number of repos of that contributer"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=toSend)

updater = Updater(token='1056953929:AAGKVZpg4OR6NgQMeGesXl9u2nfjMRJMocc', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


fork_handler = CommandHandler('forks', sendForks)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(fork_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()