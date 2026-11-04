#!/usr/bin/env python3

import os

import common
import sessions
from auth import get_cookie


def main():
    key = get_cookie(sessions.COOKIE_NAME)

    with common.db_connect() as conn:
        sessions.delete(conn, key)

    print("Status: 303 See Other")
    print("Location: /login.html")
    print(
        "Set-Cookie: session_key=; "
        "Path=/; "
        "Max-Age=0; "
        "HttpOnly; "
        "Secure; "
        "SameSite=Lax"
    )
    print()


if __name__ == "__main__":
    main()
