#!/usr/bin/env bash

# Change directory to directory where file is located
BASEDIR=$(dirname "$0")
cd $BASEDIR

# Goto and source the build-pipeline
cd ./build/code/sh
source build_pipeline.sh