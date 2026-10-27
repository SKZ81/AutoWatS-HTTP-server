import os
import sys
import traceback
import json
import urllib.parse
import sqlite3
import sessions

DATABASE_FILE="/var/www/db/database.db"
DEBUG_MODE=True

http_reason_phrases = {
    200: "OK",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error"
}

# Add info JSON object to HTTP response
def serialize_json_info(info, attributes, fout=sys.stdout):
    if not info:
        return
    fout.write("{")
    for i, attr in enumerate(attributes):
        value = info.get(attr, None)
        if value is not None:
            fout.write(f"{"" if i == 0 else ", "}\"{attr}\": \"{value}\"")
    fout.write("}\n")

# Forge an HTTP error response
def send_error(code: int, info=None):
    print("Status: %d %s"%(code, http_reason_phrases.get(code, "")))
    print("Content-Type: application/json\n")
    if not info:
        info = {}
    if "result" not in info:
        info["result"] = "failed"
    serialize_json_info(info, ["result", "reason", "sql_request", "session_key"])


def check_request_method(expected):
    request_method = os.environ.get('REQUEST_METHOD', '')
    if (request_method != expected):
        send_error(400, {"reason": "only %s allowed"%(expected)})
        sys.exit(0)

def check_session_validity(conn, session_key: str):
    if session_key is None:
        send_error(401, {"reason": "No session key provided"})
        sys.exit(0)
    if not sessions.validate(conn, session_key):
        send_error(401, {"reason": "Invalid session key", "session_key": session_key})
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


def serialize_json_data(column_names, data, unique=False):
    # Prepare JSON object
    json_data = []
    for row in data:
        row_dict = {}
        for i, value in enumerate(row):
            row_dict[column_names[i]] = value
        json_data.append(row_dict)

    json_str = json.dumps(json_data) if not unique else json.dumps(json_data[0])
    # Dump JSON plaintext
    print("Content-Type: application/json\n")
    print(json_str)


def process_SQL(sql_builder, params, on_success, check_session=False):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    if check_session:
        check_session_validity(conn, params.get("session_key", None))

    SQLRequest, error = sql_builder(params)
    if error:
        send_error(400, {"reason": error})
        sys.exit(0)

    try:
        cursor.execute(SQLRequest)
        on_success(conn, cursor)
    except Exception as e:
        # Handle other SQLite errors
        send_error(500, {"reason": str(e),
                         "sql_request": SQLRequest})
    finally:
        conn.close()


# Process an HTTP GET request.
# unique=True indicates request should return only ONE item.
@cgi_tb
def process_GET(sql_builder, unique=False):
    check_request_method("GET")
    # params = get_request_params()

    query_string = os.environ.get('QUERY_STRING', '')
    params = dict(urllib.parse.parse_qsl(query_string))

    def fetch_data(conn, cursor):
        data = cursor.fetchall()
        if len(data) == 0:
            send_error(404, {"reason": "UUID not found",
                            "sql_request": SQLrequest})
        elif unique and len(data) > 1:
            send_error(500, {"reason": "multiple entries found for UUID",
                            "sql_request": SQLrequest})
        else:
            column_names = [desc[0] for desc in cursor.description]
            serialize_json_data(column_names, data, unique)

    process_SQL(sql_builder, params, fetch_data)


# Process an HTTP POST request
@cgi_tb
def process_POST(sql_builder):
    check_request_method("POST")

    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    request_body = sys.stdin.read(content_length)
    params = json.loads(request_body)

    def commit_and_reply(conn, cursor):
        if cursor.rowcount == 0:
            send_error(404, {"reason": "UUID does not exist (or inactive)",
                             "sql_request": SQLRequest})
        else:
            conn.commit()
            print("Content-Type: application/json\n")
            print('{"result": "OK"}')

    process_SQL(sql_builder, params, commit_and_reply, check_session=True)
