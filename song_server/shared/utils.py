# Utility Functions

import os
import json
from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))


def get_secret_key():
    """
    Get a random secret string for cryptographic use
    :return: A bytes object containing random bytes
    """

    return os.urandom(24)


def populate_admin_user():
    """
    Add the admin user into the db,
    provided it doesn't already exists
    """

    from song_server.extensions.dbhelper import db_helper
    users = db_helper.get_users(is_admin_only=True)
    if len(users) > 0:
        return

    # Add the first admin user
    from song_server.models.user import User
    from song_server.models.user import UserRoles

    first_admin = User('admin', 'admin', 0,
                       user_role=UserRoles.UR_ADMIN, is_text_password=True)
    db_helper.add_item(first_admin)


def is_type_valid(value, required_type):
    """
    Check if `value` if of type `required_type` or None

    :param value: the value to be tested
    :param required_type: The accepted type of the variable
    :return: boolean, True if value if valid, False otherwise
    """

    return isinstance(value, required_type) or \
           value is None


def remove_none_keys(d):
    """
    Clean a dict of its None values,
    i.e remove all keys whose values are None

    :param d: dict to be parsed
    :return: dict, cleaned version of `d`
    """

    if d is None:
        return
    if not isinstance(d, dict):
        return

    cleaned = {key: value for key, value in d.items() if value is not None}
    return None if cleaned is {} else cleaned


def search_users_list(username, users_list):
    return next((item for item in users_list
          if item.username == username), None)
