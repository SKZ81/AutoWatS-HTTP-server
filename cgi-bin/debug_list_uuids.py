#!/usr/bin/env python3

import os
import sqlite3
import json
import common


@common.cgi_tb
def process_request():
    common.check_request_method("GET")

    conn = sqlite3.connect(common.DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT UUID FROM Plants WHERE ACTIVE=TRUE')
    data = cursor.fetchall()
    conn.close()
    column_names = [desc[0] for desc in cursor.description]

    common.do_json(column_names, data)

process_request()
