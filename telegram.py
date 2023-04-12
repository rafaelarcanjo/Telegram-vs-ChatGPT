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

        response = requests.get(self.TELEGRAM_URL + "getUpdates")
        content = response.content.decode("utf8")

        return json.loads(content)
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

        response = requests.get(self.TELEGRAM_URL + "getUpdates?offset=" + str(id + 1))
        content = response.content.decode("utf8")
        js = json.loads(content)

        if js['ok'] == True:
            return js
        else:
            return None
    # END

    def sendMessage(self, texto):
        logging.info('Function __sendMessage__')

        parse = urllib.parse.quote_plus(texto)
        url = self.TELEGRAM_URL + "sendMessage?text={}&chat_id={}".format(parse, self.TELEGRAM_ALLOW_ID)
        return requests.get(url)
    # END

    def getPermission(self, update):
        logging.info('Function __getPermission__')

        if update['message']['from']['id'] == self.TELEGRAM_ALLOW_ID \
            and not update['message']['from']['is_bot'] \
            and update['message']['chat']['type'] == 'private':
            return True
        else:
            return False
    # END

