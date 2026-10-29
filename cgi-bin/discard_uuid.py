#!/usr/bin/env python3

import common

def discardPlantUuidSQL(params):
    try:
        uuid = params["uuid"]
        return f"UPDATE PLANTS SET ACTIVE=FALSE WHERE ACTIVE=TRUE AND UUID='{uuid}'", None
    except KeyError as e:
        return None, 'UUID not found in query params'

common.process_POST(discardPlantUuidSQL)
