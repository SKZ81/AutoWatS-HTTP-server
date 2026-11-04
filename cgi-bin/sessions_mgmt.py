import argparse
import os
import sys
import logging
import sqlite3
import common
import sessions

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="session_mgmt")
    parser.add_argument(
        "--database",
        default=common.DATABASE_FILE,
    )
    # parser.add_argument(
    #     "--password",
    #     default=os.getenv("AUTOWATS_ESP32_PASSWORD"),
    # )
    # parser.add_argument(
    #     "--config-dir",
    #     default="config",
    # )

    sub = parser.add_subparsers(dest="command", required=False)

    p = sub.add_parser("create")
    p.add_argument("user_id", type=int)
    p.add_argument("--validity", "-v", type=int, default=30*60)

    p = sub.add_parser("delete")
    p.add_argument("session_id", type=str)

    p = sub.add_parser("validate")
    p.add_argument("session_key", type=str)

    p = sub.add_parser("list")

    p = sub.add_parser("clean")
    p.add_argument("--delay", "-d", type=int, default=5*60)

    return parser

if __name__ == "__main__":
    from datetime import datetime

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = build_arg_parser()
    args = parser.parse_args()
    with common.db_connect(args.database) as conn:
        # print(args)
        sessions._invalidate_expired_sessions(conn)
        if args.command == "create":
            key = sessions.create(conn, args.user_id, args.validity)
            print(f"New session key={key}")
        elif args.command == "delete":
            delete = sessions.delete(conn, args.session_id)
            print(f"{"OK" if delete else "ERROR"}: Session delete")
        elif args.command == "validate":
            valid = sessions.validate(conn, args.session_key)
            print(f"{"OK" if valid else "ERROR"}: Session {args.session} is {"" if valid else " NOT "} a valid sesion")
        elif args.command == "list":
            sessions_list = sessions.list_all(conn)
            if len(sessions_list) == 0:
                print("No session found in database.")
            else:
                for session in sessions_list:
                    print("%d. user: %s (%i), created: %s, validity:%s, valid: %s"%(
                        session["id"],
                        session["username"],
                        session["user_id"],
                        datetime.fromtimestamp(session["created_at"]),
                        session["duration"],
                        session["is_valid"],
                    ))
        elif args.command == "clean":
            sessions_cleaned = sessions._cleanup_session(conn, args.delay)
            print(f"{sessions_cleaned} session{'s' if sessions_cleaned > 1 else ''} cleaned.")
        else:
            parser.print_help()
