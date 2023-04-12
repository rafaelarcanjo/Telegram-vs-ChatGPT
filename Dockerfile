FROM python:alpine3.17

ENV FILE_SECRETS=/run/secrets/secrets.yaml
ENV DEBUG=false

RUN mkdir /app

COPY *.py /app/
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT [ "/usr/local/bin/python", "/app/main.py" ]