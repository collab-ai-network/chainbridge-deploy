#!/bin/bash

sudo apt update

sudo apt install -y python3

# get pip
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

python3 --version
pip3 --version

echo "Python 3 and pip have been installed successfully."

echo '
slack-sdk>=3.12,<4
requests
' > requirements.txt

pip3 install -r requirements.txt