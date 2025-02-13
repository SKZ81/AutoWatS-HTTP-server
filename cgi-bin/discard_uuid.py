#!/usr/bin/env python3

import os
import sys
import sqlite3
import json
import urllib
import common

@common.cgi_tb
def process_request():
    common.check_request_method("POST")

    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    request_body = sys.stdin.read(content_length)
    params = json.loads(request_body)

    SQLRequest=None

    try:
        uuid = params["uuid"]
        SQLRequest=f"UPDATE PLANTS SET ACTIVE=FALSE WHERE ACTIVE=TRUE AND UUID='{uuid}'"
    except KeyError as e:
        print("Status: 400 Bad Request")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "UUID not found in query body"}')


    try:
        conn = sqlite3.connect(common.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(SQLRequest)

        if cursor.rowcount == 0:
            print("Status: 404 Not Found")
            print("Content-Type: application/json\n")
            print('{"result": "failed", "reason": "UUID does not exist (or inactive)", "SQLquery":"%s"}'%(SQLRequest))
        else:
            conn.commit()
            print("Content-Type: application/json\n")
            print('{"result": "OK"}')
    except Exception as e:
        # Handle other SQLite errors
        print("Status: 500 Internal Server Error")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "%s", "SQLquery":"%s"}'%(str(e), SQLRequest))

    finally:
        conn.close()


process_request()
