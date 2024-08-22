#!/bin/bash

source .venv/bin/activate
cd "$(dirname "$0")"
python main.py $1
