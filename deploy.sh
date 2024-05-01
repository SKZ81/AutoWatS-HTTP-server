#!/bin/sh

set -x

. ./server.data
#    Example file:
# export SERVER_NAME=your_domain.com
# export SERVER_ROOT=/var/www/AutoWatS-HTTP

TMP=$(mktemp -d -t tmp.XXXXXXXXXX)
ssh $SERVER_NAME "mkdir -p ~/tmp"
#tar czvf $TAR_OPTS $TMP/AutoWatS-HTTP.tgz .
tar czvf $TMP/AutoWatS-HTTP.tgz $TAR_OPTS .
scp $TMP/AutoWatS-HTTP.tgz $SERVER_NAME:~/tmp
scp install-AutoWatS-HTTP.sh $SERVER_NAME:~/tmp
rm -rf $TMP
ssh $SERVER_NAME "~/tmp/install-AutoWatS-HTTP.sh $SERVER_ROOT"
ssh $SERVER_NAME "rm -rf ~/tmp"

