#!/usr/bin/env python3

import os
import sys
import sqlite3
import json
import urllib
import config

@config.cgi_tb
def process_request():
    config.check_request_method("POST")

    try:
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        request_body = sys.stdin.read(content_length)
        params = json.loads(request_body)
    except Exception as e:
        # Handle any other error
        print("Status: 500 Internal Server Error")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "%s", "SQLquery":"%s"}'%(str(e), SQLRequest))

    SQLRequest=None

    try:
        uuid = params["uuid"]
        SQLRequest=f"INSERT INTO PLANTS (UUID) VALUES ('{uuid}')"
    except KeyError as e:
        print("Status: 400 Bad Request")
        print("Content-Type: application/json\n")
        print("{'reason': 'UUID not found in query body'}")
        sys.exit(0)

    try:
        conn = sqlite3.connect(config.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(SQLRequest)
        if cursor.rowcount == 0:
            print("Status: 404 Not Found")
            print("Content-Type: application/json\n")
            print('{"result": "failed", "reason": "%s", "SQLquery":"%s"}'%(str(e), SQLRequest))
        else:
            conn.commit()
            print("Content-Type: application/json\n")
            print('{"result": "OK"}')
    except Exception as e:
        # Handle any other error
        print("Status: 500 Internal Server Error")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "%s", "SQLquery":"%s"}'%(str(e), SQLRequest))

    finally:
        # Close the database connection
        conn.close()

process_request()
