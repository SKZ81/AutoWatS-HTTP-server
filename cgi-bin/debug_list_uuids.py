#!/usr/bin/env python3

import os
import sqlite3
import json
import config

def do_html(column_names, data):
    print("""
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Simple HTML Table with Images</title>
<style>
table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
th {
    background-color: #f2f2f2;
}
img {
    width: 50px;
    height: 50px;
}
</style>
</head>
<body>

<h2>Simple HTML Table with Images</h2>

<table>
    """)

    print("  <tr>\n")
    for col in column_names:
        print("    <th>%s</th>\n"%col)
    print("  </tr>\n")
    # Prepare JSON object
    # json_data = []
    for row in data:
        # row_dict = {}
        # for i, value in enumerate(row):
        #     row_dict[column_names[i]] = value
        # json_data.append(row_dict)
        print("  <tr>\n")
        for i,value in enumerate(row):
            if i == 3:
                print("    <th><img src='/%s'></th>\n"%value)
            else:
                print("    <th>%s</th>\n"%value)
        print("  </tr>\n")

    # Dump JSON plaintext
    # json_text = json.dumps(json_data)
    # print(json_text)

    print("""
</table>

</body>
</html>
    """)

def do_json(column_names, data):
    # Prepare JSON object
    json_data = []
    for row in data:
        row_dict = {}
        for i, value in enumerate(row):
            row_dict[column_names[i]] = value
        json_data.append(row_dict)
    # Dump JSON plaintext
    print("Content-Type: application/json\n")
    print(json.dumps(json_data))


request_method = os.environ.get('REQUEST_METHOD', '')
if (request_method != 'GET'):
    print("Status: 400 Bad Request\n\n")
    sys.exit(0)

conn = sqlite3.connect(config.DATABASE_FILE)
cursor = conn.cursor()
cursor.execute('SELECT UUID FROM Plants WHERE ACTIVE=TRUE')
data = cursor.fetchall()
conn.close()
column_names = [desc[0] for desc in cursor.description]

do_json(column_names, data)
# do_html(column_names, data)
