import logging
import openai

class ChatGPT:
    def __init__(self, OPENAI_API_KEY):
        self.OPENAI_API_KEY = OPENAI_API_KEY

    def getChat(self, chat):
        logging.info('Function __getChat__')

        openai.api_key = self.OPENAI_API_KEY

        model_engine = "text-davinci-003"

        try:
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
        except openai.error.AuthenticationError as e:
            return "Erro na autenticação com o OpenAI :/"
        except Exception as e:
            return "Algo de errado não está certo :/"
    # END