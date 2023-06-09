import json
import requests
import urllib
import logging

class Telegram:
    def __init__(self, TELEGRAM_TOKEN, TELEGRAM_ALLOW_ID):
        self.TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/"
        self.TELEGRAM_ALLOW_ID = TELEGRAM_ALLOW_ID

    def getUpdates(self):
        logging.info('Function __getUpdates__')

        try:
            response = requests.get(self.TELEGRAM_URL + "getUpdates")
            content = response.content.decode("utf8")
            return json.loads(content)
        except:
            return None
    # END

    def getLastID(self, updates):
        logging.info('Function __getLastID__')
        ids = []
        
        if len(updates['result']) == 0:
            return 0
        else:
            for update in updates["result"]:
                ids.append(int(update["update_id"]))
            return max(ids)
    # END

    def getNextUpdate(self, id):
        logging.info('Function __getNextUpdate__')

        try:
            response = requests.get(self.TELEGRAM_URL + "getUpdates?offset=" + str(id + 1))
            content = response.content.decode("utf8")
            js = json.loads(content)

            if js['ok'] == True:
                return js
            else:
                return None
        except:
            return None
    # END

    def sendMessage(self, texto, update):
        logging.info('Function __sendMessage__')

        try:
            parse = urllib.parse.quote_plus(texto)
            url = self.TELEGRAM_URL + "sendMessage?text={}&chat_id={}".format(parse, str(update['message']['from']['id']))
            return requests.get(url)
        except:
            return False
    # END

    def getPermission(self, update):
        logging.info('Function __getPermission__')
        logging.debug('From: ' + str(update['message']['from']['id']))

        if str(update['message']['from']['id']) in self.TELEGRAM_ALLOW_ID \
            and not update['message']['from']['is_bot'] \
            and update['message']['chat']['type'] == 'private':
            return True
        else:
            return False
    # END
