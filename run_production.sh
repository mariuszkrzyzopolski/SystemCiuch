#!/bin/sh
export PYTHONPATH=.
python -m venv venv
venv/Scripts/python.exe -m pip install -r API/requirements.txt
venv/Scripts/python.exe -m pip install -r AI/requirements.txt
venv/Scripts/python.exe -m pip install -r Tests/requirements.txt
venv/Scripts/python.exe -m uvicorn API.main:app --host 0.0.0.0 --port 8000 &
npm run prod --prefix ./WebClient &