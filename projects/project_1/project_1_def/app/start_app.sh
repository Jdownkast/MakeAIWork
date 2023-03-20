#!/usr/bin/env bash

flask --app application --debug run  >/dev/null 2>/dev/null & 

URL="http://127.0.0.1:5000"
python -m webbrowser -t $URL 