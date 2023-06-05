import time
import yaml
import os
import logging
import sys

from telegram import Telegram
from chat import ChatGPT

ALLOW_ID        = None
OPENAI_API_KEY  = None
TELEGRAM_TOKEN  = None
DEBUG           = False

def getConfig(file=None):
    logging.info('Function __getConfig__')
    
    global ALLOW_ID
    global OPENAI_API_KEY
    global TELEGRAM_TOKEN
    global DEBUG
    
    DEBUG = (os.getenv("DEBUG") == "true")

    if file == None:
        file = "secrets.yaml"

    logging.info('Secret file: ' + file)

    with open(file, "r") as f:
        config = yaml.safe_load(f)
        
        TELEGRAM_TOKEN = config['secrets']['TELEGRAM_BOT_TOKEN']

        ALLOW_ID = config['secrets']['TELEGRAM_ALLOW_ID'].split(",")
        OPENAI_API_KEY = config['secrets']['OPENAI_API_KEY']
    # END with
# END

def main():
    logging.info('...### STARTING ###...')

    getConfig(os.getenv("FILE_SECRETS"))

    telegram = Telegram(TELEGRAM_TOKEN, ALLOW_ID)
    chatGPT = ChatGPT(OPENAI_API_KEY)

    lastID = telegram.getLastID(telegram.getUpdates())
    
    while True:
        updates = telegram.getNextUpdate(lastID)

        if (updates != None and telegram.getLastID(updates) > 1):
            lastID = telegram.getLastID(updates)
            
            for update in updates['result']:
                text = update['message']['text']

                if telegram.getPermission(update):
                    message = chatGPT.getChat(text)
                    telegram.sendMessage(message, update)
                else:
                    logging.info('Unauthorized Telegram ID')
            # END for
        time.sleep(0.5)
    # END while
# END

if __name__ == '__main__':
    if (os.getenv("DEBUG") == "true"):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    try:
        main()
    except KeyboardInterrupt:
        exit()
# END