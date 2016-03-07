#!/bin/bash

echo -e "\033[1;36mServer started. Listening 0.0.0.0:8000\033[1;0m"
python manage.py runserver -h 0.0.0.0  -p 8000