#!/usr/bin/env bash

# Start server
# MAKE PATH DYNAMIC
cd .
source ./dload_serverstart.sh
pid=$(echo "$!")

# Get data with REST API and save as csv
python dload_get_save_db.py

# Terminate server
# FIND OTHER SOLLUTION FOR TERMINATING THE SERVER
kill -9 $pid