#!/usr/bin/env python3

import common


def searchPlantSQL(params):
    try:
        uuid = params["uuid"]
        return f"""
            SELECT PLANTS.*, VARIETIES.NAME AS varietyName, VARIETIES.PHOTO_URL AS photoUrl
            FROM PLANTS
            LEFT JOIN VARIETIES ON PLANTS.VARIETY = VARIETIES.ID
            WHERE PLANTS.ACTIVE=TRUE AND  PLANTS.UUID = '{uuid}'
            """, None
    except KeyError as e:
        return None, "UUID not found in query params"


common.process_GET(searchPlantSQL, unique=True)
