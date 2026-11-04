import argparse
import os
import sys
import logging
import sqlite3
import common
import users

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="user_mgmt")
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
    p.add_argument("username", type=str)
    p.add_argument("password", type=str)
    p.add_argument("--info", "-i", type=str, default="")

    p = sub.add_parser("delete")
    p.add_argument("id", type=int)

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
    with common.db_connect(args.database) as conn:
        # print(args)
        if args.command == "create":
            user_id = users.create(conn, args.username, args.password, args.info)
            print(f"Created user {args.username} with id={user_id}")
        elif args.command == "delete":
            delete = users.delete(conn, args.id)
            print(f"{"OK" if delete else "ERROR"}: Session delete")
        elif args.command == "list":
            users_list = users.list_all(conn)
            if len(users_list) == 0:
                print("No user found in database.")
            else:
                for user in users_list:
                    print("%i. name: '%s', created: %s, validity:%s, info: %s"%(
                        user[0],
                        user[1],
                        datetime.fromtimestamp(user[3]),
                        user[4],
                        user[5],
                    ))
        else:
            parser.print_help()
