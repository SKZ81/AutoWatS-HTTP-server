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
    print("Status: 400 Bad Request\n\n")
    sys.exit(0)

content_length = int(os.environ.get('CONTENT_LENGTH', 0))
request_body = sys.stdin.read(content_length)
params = json.loads(request_body);
set_clause = ', '.join([f"{key} = '{value}'" for key, value in params.items() if key != 'UUID'])

SQLrequest = f"UPDATE Plants SET {set_clause} WHERE ACTIVE=TRUE AND UUID='{params['UUID']}'"

try:
    conn = sqlite3.connect(config.DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(SQLrequest)
    if cursor.rowcount == 0:
        print("Status: 404 Not Found")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "UUID not found", "SQLquery":"%s"}'%(SQLrequest))
    else:
        conn.commit()
        print("Content-Type: application/json\n")
        print('{"result": "OK"}')

except sqlite3.Error as e:
    # Handle other SQLite errors
    print("Status: 500 Internal Server Error")
    print("Content-Type: application/json\n")
    print('{"result": "failed", "reason": "%s", "SQLquery":"%s"}'%(str(e), SQLrequest))

finally:
    # Close the database connection
    conn.close()



