FROM python:3.8-slim-bullseye

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y libev-dev libssl-dev libffi-dev

RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
CMD [ "rasa","run", "actions" ]
