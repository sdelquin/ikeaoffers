#!/bin/bash

source ~/.pyenv/versions/ikeaoffers/bin/activate
cd "$(dirname "$0")"
python main.py $1
