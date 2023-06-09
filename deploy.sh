#!/bin/bash

source ~/.pyenv/versions/ikeaoffers/bin/activate
cd "$(dirname "$0")"
git pull
pip install -r requirements.txt
