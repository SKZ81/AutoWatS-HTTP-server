#!/usr/bin/env python3

import os
import sys
import sqlite3
import json
import urllib
import common

def createPlantUuidSQL(params):
        uuid = params["uuid"]
        return f"INSERT INTO PLANTS (UUID) VALUES ('{uuid}')"

common.process_POST(createPlantUuidSQL)
