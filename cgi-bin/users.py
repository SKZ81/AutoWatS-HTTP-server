import hashlib
import secrets
import sqlite3
import time

def hash_password(password):
    salt = secrets.token_bytes(16)

    hashed = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=2**14,
        r=8,
        p=1
    )

    return "scrypt${}${}".format(
        salt.hex(),
        hashed.hex()
    )


def verify_password(password, stored_hash):
    try:
        algorithm, salt_hex, hash_hex = stored_hash.split("$")

        if algorithm != "scrypt":
            return False

        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)

        actual = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=2**14,
            r=8,
            p=1
        )

        return secrets.compare_digest(actual, expected)

    except (ValueError, TypeError):
        return False


def create(conn: sqlite3.Connection,
           username: str, password: str,
           info: str = ""
) -> int:
    pwd_hash = hash_password(password)

    cursor = conn.execute(
        """
        INSERT INTO Users (username, pwd_hash, created_at, is_valid, info)
        VALUES (?, ?, ?, 1, ?)
        """,
        (username,
         pwd_hash,
         int(time.time()),
         info)
    )

    return cursor.lastrowid


def authenticate(conn: sqlite3.Connection,
                 username: str, password: str
) -> int | None:
    user = conn.execute(
        """
        SELECT id, pwd_hash
        FROM Users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    if user is None:
        return None

    if not verify_password(password, user["pwd_hash"]):
        return None

    return user["id"]


def update(conn: sqlite3.Connection, user_id: int,
           username: str=None, password: str=None):
    if username is not None:
        conn.execute(
            """
            UPDATE Users
            SET username = ?
            WHERE id = ?
            """,
            (username,
             user_id)
        )

    # TODO: invalidate any session open for this user
    if password is not None:
        conn.execute(
            """
            UPDATE Users
            SET pwd_hash = ?
            WHERE id = ?
            """,
            (hash_password(password),
             user_id)
        )


def delete(conn: sqlite3.Connection, user_id: int):
    cursor = conn.execute(
        """
        DELETE FROM Users
        WHERE id = ?
        """, (user_id,)
    )

    return cursor.rowcount > 0


def list_all(conn):
    # Return all existing users
    res = conn.execute(
        """
        SELECT *
        FROM Users
        """
    )

    return list(res)
