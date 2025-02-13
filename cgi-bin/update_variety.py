#!/usr/bin/env python3

import os
import sys
import sqlite3
# import cgi
import json
import urllib
import config


@config.cgi_tb
def process_request():
    config.check_request_method("POST")

    try:
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        request_body = sys.stdin.read(content_length)
        params = json.loads(request_body);
        set_clause = ', '.join([f"{key} = '{value}'" for key, value in params.items() if key != 'id'])

        SQLrequest = f"UPDATE Varieties SET {set_clause} AND id='{params['id']}'"

        conn = sqlite3.connect(config.DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute(SQLrequest)
        if cursor.rowcount == 0:
            print("Status: 404 Not Found")
            print("Content-Type: application/json\n")
            print('{"result": "failed", "reason": "id not found", "SQLquery":"%s"}'%(SQLrequest))
        else:
            conn.commit()
            print("Content-Type: application/json\n")
            print('{"result": "OK"}')

    except Exception as e:
        # Handle other errors
        print("Status: 500 Internal Server Error")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "%s", "SQLquery":"%s"}'%(str(e), SQLrequest))

    finally:
        conn.close()


process_request()
