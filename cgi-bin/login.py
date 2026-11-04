#!/usr/bin/env python3

import os
import sys
from urllib.parse import parse_qs

import users
import sessions
import common
import sqlite3
import json

# TODO : respond() should be in 'common'

def respond(status, headers=None):
    print(f"Status: {status}")
    if headers is None or "Content-Type" not in headers:
        print("Content-Type: application/json; charset=utf-8")

    if headers:
        for key, value in headers.items():
            print(f"{key}: {value}")

    print()

@common.cgi_tb
def main():
    try:
        length = int(os.environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        respond("400 Bad Request")
        return

    if length > 4096:
        respond("413 Payload Too Large")
        return

    try:
        body = sys.stdin.read(length)
        params = json.loads(body)

        if not isinstance(params, dict):
            raise ValueError("JSON object expected")

    except (json.JSONDecodeError, ValueError):
        respond("400 Bad Request")
        return

    username = params.get("username", "")
    password = params.get("password", "")

    if not isinstance(username, str) or not isinstance(password, str):
        respond("400 Bad Request")
        return

    with common.db_connect() as conn:
        user_id = users.authenticate(conn, username, password)

        if user_id is None:
            respond("401 Unauthorized")
            return

        key = sessions.create(conn, user_id)

        http_cookie = os.environ.get("HTTP_COOKIE", "0") == "1"
        respond("200 OK", {
            "Content-Type": "application/json; charset=utf-8",
            "Set-Cookie": (
                f"session_key={key}; "
                "Path=/; "
                "Max-Age=1800; "
                "HttpOnly; " if not http_cookie else ""
                "Secure; "
                "SameSite=Lax"
            )
        })
        print("{\"result\": \"OK\"}")

if __name__ == "__main__":
    main()
    # print("Status: 418 I'm a teapot")
    # print("Content-Type: text/plain")
    # print()
    # print("Hello from CGI!")
