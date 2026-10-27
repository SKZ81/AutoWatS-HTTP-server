#!/usr/bin/env python3

import os
import sys
import sqlite3
import json
import urllib
import common


def updatePlantSQL(params):
    try:
        set_clause = ', '.join([f"{key} = '{value}'" for key, value in params.items() if key != 'UUID'])
        SQLrequest = f"UPDATE Plants SET {set_clause} WHERE ACTIVE=TRUE AND UUID='{params['UUID']}'"
    except KeyError as e:
        return None, 'UUID not found in query body'

common.process_request(updatePlantSQL)
