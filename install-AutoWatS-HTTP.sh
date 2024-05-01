#!/bin/sh

set -x

SERVER_ROOT=$1

TMP_DIR=$(mktemp -d -t tmp.XXXXXXXXXX)
cd $TMP_DIR
tar xvf ~/tmp/AutoWatS-HTTP.tgz .

sudo cp -r cgi-bin $SERVER_ROOT/
sudo cp -r images $SERVER_ROOT/
sudo sqlite3 $SERVER_ROOT/db/database.db ".read $TMP_DIR//db/database.sql"

#sudo scp -r etc/systemd/system/nginx.service.d/local.conf /etc/systemd/system/nginx.service.d/local.conf
#     Example file:
# [Service]
# Environment="SERVER_NAME=your_domain.com"

sudo cp etc/nginx/nginx.conf /etc/nginx/nginx.conf
sudo cp etc/nginx/sites-available/AutoWatS-HTTP /etc/nginx/sites-available/AutoWatS-HTTP
sudo cp etc/systemd/system/nginx.service.d/local.conf /etc/systemd/system/nginx.service.d/local.conf

sudo systemctl daemon-reload
sudo systemctl restart nginx.service

cd
rm -rf $TMP_DIR
