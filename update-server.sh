#!/bin/bash

supervisorctl shutdown

cd logs
unalias rm
sudo rm -rf *err* *out*
cd -

git pull

pybabel compile -d app/translations

supervisord

supervisorctl start all

sleep 10
supervisorctl status
