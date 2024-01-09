import logging
from openai import OpenAI

class ChatGPT:
    def __init__(self, OPENAI_API_KEY):
        self.OPENAI_API_KEY = OPENAI_API_KEY

    def getChat(self, chat):
        logging.info('Function __getChat__')

        client = OpenAI(api_key=self.OPENAI_API_KEY)

        try:
            completions = client.chat.completions.create(
                model="gpt-4",
                max_tokens=512,
                temperature=0.1,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=1,
                n=1,
                stop=None,
                messages=[{"role": "user", "content": chat}]
            )

            return completions.choices[0].message.content
        except Exception as e:
            return "Algo de errado não está certo :/"
    # END