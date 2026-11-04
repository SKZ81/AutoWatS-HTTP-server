#!/usr/bin/env python3

import os
import sys

import common
import sessions

from http.cookies import SimpleCookie

def get_cookie(name):
    cookie = SimpleCookie()
    cookie.load(os.environ.get("HTTP_COOKIE", ""))

    morsel = cookie.get(name)

    return morsel.value if morsel else None

def main():
    key = get_cookie(sessions.COOKIE_NAME)

    with common.db_connect() as conn:
        if sessions.validate(conn, key):
            print("Status: 204 No Content")
        else:
            print("Status: 401 Unauthorized")

    print()

if __name__ == "__main__":
    main()
