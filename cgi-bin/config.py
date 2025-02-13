import os
import sys
import traceback

DATABASE_FILE="/var/www/db/database.db"
DEBUG_MODE=True

def check_request_method(expected):
    request_method = os.environ.get('REQUEST_METHOD', '')
    if (request_method != expected):
        print("Status: 400 Bad Request")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "only %s allowed"}'%(expected))
        sys.exit(0)

def cgi_tb(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Status: 500 Internal Server Error")
            print("Content-Type: text/html\n")
            print("<h1>Internal Server Error</h1>")
            print("<pre>")
            print("An error occurred during request processing...\n")
            if DEBUG_MODE:
                print(traceback.format_exc())
            print("</pre>")
            return None
    return wrapper


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
