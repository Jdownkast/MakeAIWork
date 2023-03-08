#!/usr/bin/env bash

port=8080
url="http://localhost:$port/medish_centrum_randstad/api/netlify"

printf "Start django application at %s\n" ${url}
python ../from_miw/rest_server/medisch_centrum_randstad/manage.py runserver 0.0.0.0:${port} &