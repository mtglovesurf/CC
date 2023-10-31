#!/bin/bash

mkdir db
chmod 777 db

mkdir -p redmine/files
mkdir -p redmine/log
mkdir -p redmine/plugins
mkdir -p redmine/themes
chmod -R 777 redmine

echo -n input docker-hub username:
read user
echo -n input password:
read pass

sudo docker login -u user -p pass
sudo docker-compose up -d
sudo docker logout
