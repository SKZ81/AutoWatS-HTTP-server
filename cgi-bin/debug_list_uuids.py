#!/usr/bin/env python3

import common


@common.cgi_tb
def debugListUuidsSQL(params):
    return "SELECT UUID FROM Plants WHERE ACTIVE=TRUE", None

common.process_GET(debugListUuidsSQL)
