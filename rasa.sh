#!/bin/bash

# Activate virtual environment
source .venv/bin/activate
pip install -r requirements.txt

rasa train

# Run Rasa actions server
rasa run actions &

# Run Rasa API server
rasa run --enable-api --cors "*"

# Deactivate virtual environment
deactivate
