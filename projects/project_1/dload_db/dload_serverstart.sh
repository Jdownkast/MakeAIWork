#!/usr/bin/env bash

port=8080
start_page=1
url="http://localhost:$port/medisch_centrum_randstad/api/netlify?page=$start_page"

printf "Start django application at %s\n" ${url}
python ../_from_miw/rest_server_new/medisch_centrum_randstad/manage.py runserver 0.0.0.0:${port} &