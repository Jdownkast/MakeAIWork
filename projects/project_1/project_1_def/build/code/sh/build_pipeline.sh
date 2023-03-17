#!/usr/bin/env bash

# Start and close server to download data
source dload_db.sh

# Transform dataset and train model
cd ../python
python tform_ds.py
python train_model.py