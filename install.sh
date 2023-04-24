#!/bin/sh
virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
rasa train
echo 'Instalação finalizada'
