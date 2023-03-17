#!/usr/bin/env bash

# Start server
source dload_serverstart.sh
pid=$(echo "$!")

# Get data with REST API and save as csv
cd ../python
python dload_get_save_db.py

# Back to build.sh dir and terminate server
cd ../..
kill -9 $pid