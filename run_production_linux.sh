#!/bin/sh

python3 -m venv venv

export PYTHONPATH=$PYTHONPATH:./

if [ "$1" = "-i" ]; then
  venv/bin/python3 -m pip install -r API/requirements.txt
  venv/bin/python3 -m pip install -r AI/requirements.txt
  venv/bin/python3 -m pip install -r Tests/requirements.txt
fi

npm run prod --prefix ./WebClient &
pid1=$!

export URL=""
venv/bin/python3 -m uvicorn API.main:app --host 0.0.0.0 --port 8000

wait -n
kill $pid1
