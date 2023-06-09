#!/bin/sh
export PYTHONPATH=.
uvicorn API.main:app --host 0.0.0.0 --port 8000 &
npm run prod --prefix ./WebClient &