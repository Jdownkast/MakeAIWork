#!/usr/bin/env bash

cd ./Projects/project_1/dload_db
source dload_db.sh

cd ../tform_db
python tform_db.py

cd ../train_model
python train_model.py

cd ../../..