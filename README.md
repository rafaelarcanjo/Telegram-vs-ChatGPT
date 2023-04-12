# Telegram Chatbot with OpenAI API Integration

Este arquivo contém as instruções para a execução do bot do Telegram com integração via API da OpenAI.

## Pré-requisitos
Antes de começar, certifique-se de que você tenha o Python 3.7 ou superior, ou o Docker e Docker Compose instalado em seu computador.

## Passo a passo
1. Renomeie o arquivo `secrets.example.yaml` para `secrets.yaml`;
2. Adicione o seu ID do Telegram na variável `TELEGRAM_ALLOW_ID`;
3. Adicione a sua API_KEY da OpenAI na variável `OPENAI_API_KEY`;
4. Adicione o token do seu bot do Telegram na variável `TELEGRAM_BOT_TOKEN`.

## Execução com Python
1. Abra o terminal e navegue até o diretório que contém os arquivos;
2. Execute o comando `pip install -r requirements.txt` para instalar as dependências necessárias;
3. Execute o comando `python3 main.py` para iniciar o programa.

## Execução com Docker
1. Abra o terminal e navegue até o diretório que contém os arquivos;
2. Execute o comando `docker-compose up -d --build`.


## Observações
- Certifique-se de que seu computador esteja conectado à internet durante a instalação das dependências.
- É recomendado a execução pelo Docker.

----
Rafael Silva
rafael@libre.tec.br
https://www.libre.tec.br