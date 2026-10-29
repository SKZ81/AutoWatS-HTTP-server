#!/usr/bin/env python3

import uuid
import common

def createPlantUuidSQL(params):
    try:
        uuid = params.get("uuid", str(uuid.uuid4())
        return f"INSERT INTO PLANTS (UUID) VALUES ('{uuid}')", None
    # except KeyError as e:
    #     return None, "UUID not found in query params"

common.process_POST(createPlantUuidSQL)
