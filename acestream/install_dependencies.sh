#!/bin/sh

sudo apt-get update
sudo apt-get install -y python3-pip libpython3.10

# upgrade pip
python3.10 -m pip install --upgrade pip

# install dependencies
python3.10 -m pip install -r requirements.txt
