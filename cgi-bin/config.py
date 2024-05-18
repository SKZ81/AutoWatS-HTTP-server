DATABASE_FILE="/var/www/AutoWatS-HTTP/db/database.db"

# Comment the following to improve security in production environment
import cgitb
cgitb.enable() #disable in prod !!!

import os
def check_request_method(expected):
    request_method = os.environ.get('REQUEST_METHOD', '')
    if (request_method != expected):
        print("Status: 400 Bad Request")
        print("Content-Type: application/json\n")
        print('{"result": "failed", "reason": "only %s allowed"}'%(expected))
        sys.exit(0)
