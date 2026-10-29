#!/usr/bin/env python3

import common


def createVarietySQL(params):
    try:
        value_clause = f'({params.get("name", "")}, {params.get("short_descr", "")}, {params.get("blooming_time_days", "")})'
        uuid = params["uuid"]
        return f"INSERT INTO Varieties (name, short_descr, blooming_time_days) VALUES ('{uuid}')", None
    except KeyError as e:
        return None, "UUID not found in query params"

common.process_POST(createVarietySQL)
