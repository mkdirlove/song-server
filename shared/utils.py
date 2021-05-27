# Utility Functions

import os
import json
from bson import json_util

from models.user import User
from models.user import UserRoles


def parse_json(data):
    return json.loads(json_util.dumps(data))


def get_secret_key():
    return os.urandom(24)


def populate_admin_user():
    """
    Add the admin user into the db,
    provided it doesn't already exists
    """

    from extensions.dbhelper import db_helper
    users = db_helper.get_users(is_admin_only=True)
    if len(users) > 0:
        return

    # Add the first admin user
    first_admin = User('admin', 'admin', 0,
                       user_role=UserRoles.UR_ADMIN, is_text_password=True)
    db_helper.add_item(first_admin)
