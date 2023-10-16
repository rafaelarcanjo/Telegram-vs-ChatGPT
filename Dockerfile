FROM python:3.11-alpine3.18

ENV FILE_SECRETS=/run/secrets/secrets.yaml
ENV DEBUG=false

RUN mkdir /app

COPY *.py /app/
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT [ "/usr/local/bin/python", "/app/main.py" ]