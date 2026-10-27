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
    p.add_argument("--info", "-i", type=str, default="")
    p.add_argument("--validity", "-v", type=int, default=30*60)

    p = sub.add_parser("delete")
    p.add_argument("session", type=str)

    p = sub.add_parser("validate")
    p.add_argument("session", type=str)

    p = sub.add_parser("list")

    return parser

if __name__ == "__main__":
    from datetime import datetime

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = build_arg_parser()
    args = parser.parse_args()
    with sqlite3.connect(args.database) as conn:
        # print(args)
        sessions._invalidate_expired_sessions(conn)
        if args.command == "create":
            key = sessions.create(conn, args.validity, args.info)
            print(f"New session key={key}")
        elif args.command == "delete":
            delete = sessions.delete(conn, args.session)
            print(f"{"OK" if delete else "ERROR"}: Session delete")
        elif args.command == "validate":
            valid = sessions.validate(conn, args.session)
            print(f"{"OK" if valid else "ERROR"}: Session {args.session} is {"" if valid else " NOT "} a valid sesion")
        elif args.command == "list":
            sessions_list = sessions.list_all(conn)
            if len(sessions_list) == 0:
                print("No session found in database.")
            else:
                for session in sessions_list:
                    print("%d. key: '%s', created: %s, validity:%s, valid: %s (%s)"%(
                        session[0],
                        session[1],
                        datetime.fromtimestamp(session[2]),
                        session[3],
                        session[4],
                        session[5],
                    ))
        else:
            parser.print_help()
