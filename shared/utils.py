# Utility Functions

import os
import json
from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))


def get_secret_key():
    return os.urandom(24)
