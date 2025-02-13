#!/usr/bin/env python3

import os
import sqlite3
import json
import config


@config.cgi_tb
def process_request():
    config.check_request_method("GET")

    conn = sqlite3.connect(config.DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM varieties')
    data = cursor.fetchall()
    conn.close()
    column_names = [desc[0] for desc in cursor.description]

    config.do_json(column_names, data)

process_request()
