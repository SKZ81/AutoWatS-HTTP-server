#!/usr/bin/env python3

import common


def updatePlantSQL(params):
    try:
        set_clause = ', '.join([f"{key} = '{value}'" for key, value in params.items() if key != 'UUID'])
        uuid = params['UUID']
        return f"UPDATE Plants SET {set_clause} WHERE ACTIVE=TRUE AND UUID='{uuid}'", None
    except KeyError as e:
        return None, 'UUID not found in query params'

common.process_POST(updatePlantSQL)
