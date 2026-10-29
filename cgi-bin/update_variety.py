#!/usr/bin/env python3

import common

def updateVarietySQL(params):
    try:
        set_clause = ', '.join([f"{key} = '{value}'" for key, value in params.items() if key != 'id'])
        uuid = params['UUID']
        return f"UPDATE Plants SET {set_clause} WHERE ACTIVE=TRUE AND UUID='{uuid}'", None
    except KeyError as e:
        return None, "variety's id not found in query params"

common.process_POST(updateVarietySQL)
