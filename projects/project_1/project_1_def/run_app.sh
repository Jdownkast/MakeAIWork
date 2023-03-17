#!/usr/bin/env bash

# Change directory to directory where file is located
BASEDIR=$(dirname "$0")
# cd $BASEDIR
cd ~/MakeAIWork/projects/project_1/project_1_def

# Start application (flask development server)
cd ./app
source start_app.sh >/dev/null 2>/dev/null

# Go back to original path
cd ..

# Keep server alive for period of time
ALIVEMIN=10 # Minutes before server times out
COUNTER=0

while [[ $ALIVEMIN > $COUNTER ]]
do
    echo "Server will time out in $(($ALIVEMIN-$COUNTER)) minutes"
    sleep 60
    COUNTER=$((COUNTER + 1))
done