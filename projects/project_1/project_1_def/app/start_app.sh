#!/usr/bin/env bash

flask --app application --debug run &

URL="http://127.0.0.1:5000"
python -m webbrowser -t $URL 