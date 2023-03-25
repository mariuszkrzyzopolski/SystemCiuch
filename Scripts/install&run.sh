#!/bin/bash

python3 -m venv ../venv
source .venv/bin/activate
pip install -r ../AI/requirements.txt
pip install -r ../API/requirements.txt
python3 ../API/main.py