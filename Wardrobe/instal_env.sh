#!/bin/bash

sudo apt-get install python3-venv
python3 -m venv venv
source ./venv/bin/activate
export PYTHONPATH=$PYTHONPATH:~/SystemCiuch
pip install -r Wardrobe/requirements.txt 
python3 shelf_controller.py
