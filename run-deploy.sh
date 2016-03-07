#!/bin/bash

echo -e "\033[1;36mServer started.[1;0m"
gunicorn manage:app -c gunicorn.conf