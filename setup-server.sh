#!/bin/bash

sudo apt-get update
# For basic
sudo apt-get install -y python-pip python-dev libmysqlclient-dev
# For pillow
sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

sudo pip install requirements.txt
