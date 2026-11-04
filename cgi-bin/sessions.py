
import hashlib
import secrets
import sqlite3
import time


SESSION_DURATION = 1800
COOKIE_NAME = "session_key"


def _generate_key() -> str:
    return secrets.token_urlsafe(32)


def _hash_key(key) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def _cleanup_session(conn: sqlite3.Connection,
                     delay: int = 300
) -> int:
    """Clean invalid sessions from database after delay."""
    now = int(time.time())

    cursor = conn.execute(
        """
        DELETE FROM Sessions
        WHERE is_valid = 0
            AND duration > 0
            AND created_at + duration + ? <= ?
        """,
        (delay, now,),
    )

    return cursor.rowcount


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



def create(conn: sqlite3.Connection,
           user_id: int,
           duration: int=SESSION_DURATION
) -> str:
    if duration < 0:
        raise ValueError("Session duration cannot be negative")

    key = _generate_key()

    conn.execute(
        """
        INSERT INTO Sessions
            (key_hash, user_id, created_at, duration)
        VALUES (?, ?, ?, ?)
        """, (
        _hash_key(key),
        user_id,
        int(time.time()),
        duration
    ))

    return key


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

def delete(conn: sqlite3.Connection, session_id: int) -> bool:
    """
    Completely remove a session.
    Return True if a session was found and deleted.
    """
    # key_hash = _hash_key(session_key)

    cursor = conn.execute(
        """
        DELETE FROM Sessions
        WHERE id = ?
        """,
        (session_id,)
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
        SELECT id
        FROM Sessions
        WHERE key_hash = ?
            AND is_valid = 1
            AND (
                duration = 0
                OR created_at + duration > ?
            )
        """,
        (key_hash, int(time.time())
    )).fetchone()

    return row is not None

def list_all(conn: sqlite3.Connection) -> list:
    """
    Return all existing sessions
    """
    cursor = conn.execute(
        """
        SELECT Sessions.*, Users.username
        FROM Sessions
        LEFT JOIN Users ON Sessions.user_id = Users.id;
        """
    )
    rows =  cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    sessions = [{column_names[i]: value for i, value in enumerate(row)} for row in rows]
    print(sessions)
    return sessions


