import os
import sys
import traceback
import json

DATABASE_FILE="/var/www/db/database.db"
DEBUG_MODE=True

def check_request_method(expected):
    request_method = os.environ.get('REQUEST_METHOD', '')
    if (request_method != expected):
        print("Status: 400 Bad Request")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "only %s allowed"}'%(expected))
        sys.exit(0)

# CGI TraceBack wrapper allow to embed the error backtrace
# into the HTML response when decorated func fails.
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

@cgi_tb
def process_POST(sql_builder):
    check_request_method("POST")

    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    request_body = sys.stdin.read(content_length)
    params = json.loads(request_body)

    try:
        SQLRequest, error = sql_builder(params)
        if error:
            print("Status: 400 Bad Request")
            print("Content-Type: application/json\n")
            print('{"result": "failed", "reason": "%s"}'%error)

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
