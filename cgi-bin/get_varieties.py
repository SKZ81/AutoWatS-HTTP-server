#!/usr/bin/env python3

import common


@common.cgi_tb
def getVarietiesSQL(params):
    return "SELECT * FROM varieties", None

common.process_GET(getVarietiesSQL)
