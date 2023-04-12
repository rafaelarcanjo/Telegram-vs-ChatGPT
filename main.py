import json
import requests
import time
import openai
import urllib
import yaml
import os
import logging
import sys

TELEGRAM_URL    = None
ALLOW_ID        = None
OPENAI_API_KEY  = None

def getUpdates():
    logging.info('Function __getUpdates__')

    response = requests.get(TELEGRAM_URL + "getUpdates")
    content = response.content.decode("utf8")

    return json.loads(content)
# END

def getLastID(updates):
    logging.info('Function __getLastID__')
    ids = []
    
    if len(updates['result']) == 0:
        return 0
    else:
        for update in updates["result"]:
            ids.append(int(update["update_id"]))
        return max(ids)
# END

def getNextUpdate(id):
    logging.info('Function __getNextUpdate__')

    response = requests.get(TELEGRAM_URL + "getUpdates?offset=" + str(id + 1))
    content = response.content.decode("utf8")
    js = json.loads(content)

    if js['ok'] == True:
        return js
    else:
        return None
# END

def getChatGPT(chat):
    logging.info('Function __getChatGPT__')

    openai.api_key = OPENAI_API_KEY

    model_engine = "text-davinci-003"

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=chat,
        max_tokens=512,
        temperature=0.1,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=1,
        n=1,
        stop=None
    )

    return completions.choices[0].text[:4000]
# END

def sendMessage(texto):
    logging.info('Function __sendMessage__')

    parse = urllib.parse.quote_plus(texto)
    url = TELEGRAM_URL + "sendMessage?text={}&chat_id={}".format(parse, ALLOW_ID)
    return requests.get(url)
# END

def getPermission(update):
    logging.info('Function __getPermission__')

    if update['message']['from']['id'] == ALLOW_ID \
        and not update['message']['from']['is_bot'] \
        and update['message']['chat']['type'] == 'private':
        return True
    else:
        return False
# END

def getConfig(file=None):
    logging.info('Function __getConfig__')
    
    if file == None:
        file = "secrets.yaml"

    logging.info('Secret file: ' + file)

    with open(file, "r") as f:
        config = yaml.safe_load(f)

        global TELEGRAM_URL
        global ALLOW_ID
        global OPENAI_API_KEY
        
        token = config['secrets']['TELEGRAM_BOT_TOKEN']
        TELEGRAM_URL = "https://api.telegram.org/bot" + token + "/"

        ALLOW_ID = config['secrets']['TELEGRAM_ALLOW_ID']
        OPENAI_API_KEY = config['secrets']['OPENAI_API_KEY']
# END

def main():
    logging.info('...### STARTING ###...')

    getConfig(os.getenv("FILE_SECRETS"))

    lastID = getLastID(getUpdates())
    
    while True:
        updates = getNextUpdate(lastID)

        if (updates != None and getLastID(updates) > 1):
            lastID = getLastID(updates)
            
            for update in updates['result']:
                text = update['message']['text']

                if getPermission(update):
                    message = getChatGPT(text)
                else:
                    logging.info('Unauthorized Telegram ID')
                    message = 'Sai daqui mano!'

                sendMessage(message)
        
        time.sleep(0.5)
# END

if __name__ == '__main__':
    if os.getenv("DEBUG") == "true":
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    try:
        main()
    except KeyboardInterrupt:
        exit()
# END