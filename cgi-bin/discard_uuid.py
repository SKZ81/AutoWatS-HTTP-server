#!/usr/bin/env python3

import os
import sys
import sqlite3
import json
import urllib
import common

def discardPlantUuidSQL(params):
    try:
        uuid = params["uuid"]
        return f"UPDATE PLANTS SET ACTIVE=FALSE WHERE ACTIVE=TRUE AND UUID='{uuid}'"
    except KeyError as e:
        return None, 'UUID not found in query body'

common.process_request(discardPlantUuidSQL)
