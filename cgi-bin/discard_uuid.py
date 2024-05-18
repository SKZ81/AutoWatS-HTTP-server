#!/usr/bin/env python3

import os
import sys
import sqlite3
import cgi
import json
import urllib
import config

# Get the request method (GET or POST)
request_method = os.environ.get('REQUEST_METHOD', '')
if (request_method != 'POST'):
    print("Status: 400 Bad Request")
    print("Content-Type: application/json\n")
    print('{"result": "failed", "reason": "only POST allowed"}')
    sys.exit(0)
content_length = int(os.environ.get('CONTENT_LENGTH', 0))
request_body = sys.stdin.read(content_length)


# query_string = os.environ.get('QUERY_STRING', '')
# params = urllib.parse.parse_qs(query_string)
# uuid = params.get('uuid', [''])[0]
params = json.loads(request_body)

SQLRequest=None

try:
    uuid = params["uuid"]
    SQLRequest=f"UPDATE PLANTS SET ACTIVE=FALSE WHERE ACTIVE=TRUE AND UUID='{uuid}'"
except KeyError as e:
    print("Status: 400 Bad Request")
    print("Content-Type: application/json\n")
    print('{"result": "failed", "reason": "UUID not found in query body"}')


conn = sqlite3.connect(config.DATABASE_FILE)
cursor = conn.cursor()

try:
    cursor.execute(SQLRequest)
    if cursor.rowcount == 0:
        print("Status: 404 Not Found")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "UUID does not exist (or inactive)", "SQLquery":"%s"}'%(SQLRequest))
    else:
        conn.commit()
        print("Content-Type: application/json\n")
        print('{"result": "OK"}')
except sqlite3.Error as e:
    # Handle other SQLite errors
    print("Status: 500 Internal Server Error")
    print("Content-Type: application/json\n")
    print('{"result": "failed", "reason": "%s", "SQLquery":"%s"}'%(str(e), SQLRequest))

finally:
    # Close the database connection
    conn.close()


