
import hashlib
import secrets
import sqlite3
import time


def _hash_key(session_key: str) -> str:
    """Return the SHA-256 hash of a session key."""
    return hashlib.sha256(session_key.encode("utf-8")).hexdigest()


def _invalidate_expired_sessions(conn: sqlite3.Connection) -> None:
    """Invalidate all expired sessions."""
    now = int(time.time())

    conn.execute(
        """
        UPDATE Sessions
        SET is_valid = 0
        WHERE is_valid = 1
            AND duration > 0
            AND created_at + duration <= ?
        """,
        (now,),
    )


def create(
    conn: sqlite3.Connection,
    duration: int = 0,
    info: str = "",
) -> str:
    """
    Create a session and return its secret key.

    duration: validity duration in seconds; 0 means no expiration.
    info: free-text information associated with the session.
    """
    if duration < 0:
        raise ValueError("Session duration cannot be negative")

    session_key = secrets.token_hex(32)
    key_hash = _hash_key(session_key)
    now = int(time.time())

    conn.execute(
        """
        INSERT INTO Sessions
            (key_hash, created_at, duration, is_valid, info)
        VALUES (?, ?, ?, 1, ?)
        """,
        (key_hash, now, duration, info),
    )

    return session_key


def invalidate(conn: sqlite3.Connection, session_key: str) -> bool:
    """
    Invalidate a session.
    Return True if an active session was found and invalidated.
    """
    key_hash = _hash_key(session_key)

    cursor = conn.execute(
        """
        UPDATE Sessions
        SET is_valid = 0
        WHERE key_hash = ?
            AND is_valid = 1
        """,
        (key_hash,),
    )

    return cursor.rowcount > 0

def delete(conn: sqlite3.Connection, session_key: str) -> bool:
    """
    Completely remove a session.
    Return True if a session was found and deleted.
    """
    key_hash = _hash_key(session_key)

    cursor = conn.execute(
        """
        DELETE FROM Sessions
        WHERE key_hash = ?
        """,
        (key_hash,),
    )

    return cursor.rowcount > 0

def validate(conn: sqlite3.Connection, session_key: str) -> bool:
    """
    Invalidate expired sessions, then validate the supplied key.
    Return True only for a valid session.
    """
    if not isinstance(session_key, str) or not session_key:
        return False

    _invalidate_expired_sessions(conn)

    key_hash = _hash_key(session_key)

    row = conn.execute(
        """
        SELECT 1
        FROM Sessions
        WHERE key_hash = ?
            AND is_valid = 1
        LIMIT 1
        """,
        (key_hash,),
    ).fetchone()

    return row is not None

def list_all(conn: sqlite3.Connection) -> list:
    """
    Return all existing sessions
    """

    res = conn.execute(
        """
        SELECT *
        FROM Sessions
        """
    )

    return list(res)
