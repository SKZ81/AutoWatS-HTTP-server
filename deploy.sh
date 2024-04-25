#!/bin/sh

. server.data
#    Example file:
# export SERVER_NAME=your_domain.com
# export SERVER_ROOT=/var/www/AutoWatS-HTTP

sudo scp -r cgi-bin/ $SERVER_NAME:$SERVER_ROOT/
sudo scp -r images/ $SERVER_NAME:$SERVER_ROOT/
sudo scp -r db/ $SERVER_NAME:$SERVER_ROOT/

#sudo scp -r etc/systemd/system/nginx.service.d/local.conf /etc/systemd/system/nginx.service.d/local.conf
#     Example file:
# [Service]
# Environment="SERVER_NAME=your_domain.com"

sudo scp -r etc/nginx/nginx.conf $SERVER_NAME:/etc/nginx/nginx.conf
sudo scp -r etc/nginx/sites-available/AutoWatS-HTTP $SERVER_NAME:/etc/nginx/sites-available/AutoWatS-HTTP

