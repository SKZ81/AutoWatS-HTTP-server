#!/usr/bin/env python3

import os
import sys
import sqlite3
import json
import urllib
import urllib.parse
import config


@config.cgi_tb
def process_request():
    config.check_request_method("GET")

    query_string = os.environ.get('QUERY_STRING', '')
    params = urllib.parse.parse_qs(query_string)
    uuid = params.get('uuid', [''])[0]

    conn = sqlite3.connect(config.DATABASE_FILE)
    cursor = conn.cursor()
    SQLrequest = f"""
    SELECT PLANTS.*, VARIETIES.NAME AS varietyName, VARIETIES.PHOTO_URL AS photoUrl
    FROM PLANTS
    LEFT JOIN VARIETIES ON PLANTS.VARIETY = VARIETIES.ID
    WHERE PLANTS.ACTIVE=TRUE AND  PLANTS.UUID = '{uuid}'
    """

    cursor.execute(SQLrequest)
    data = cursor.fetchall()
    conn.close()

    if len(data) == 0:
        print("Status: 404 Not Found")
        print("Content-Type: application/json\n")
        print("{'reason': 'UUID not found', 'request':'" + SQLrequest + "'}")
    elif len(data) > 1:
        print("Status: 500 Internal Server Error")
        print("Content-Type: application/json\n")
        print("{'reason': 'multiple entries found for UUID', 'request':'" + SQLrequest + "'}")
    else:
        column_names = [desc[0] for desc in cursor.description]
        config.do_json(column_names, data[0])


process_request()
