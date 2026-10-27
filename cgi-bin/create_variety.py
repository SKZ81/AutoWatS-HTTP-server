#!/usr/bin/env python3

import os
import sys
import sqlite3
import json
import urllib
import common


def createVarietySQL(params):
    try:
        def get_param(param):
            return params.get(param) or "\'\'"
        value_clause = f'({get_param("name")}, {get_param("short_descr")}, {get_param("blooming_time_days")})'
        uuid = params["uuid"]
        return f"INSERT INTO Varieties (name, short_descr, blooming_time_days) VALUES ('{uuid}')"
    except KeyError as e:
        return None, 'UUID not found in query body'

common.process_POST(createVarietySQL)
