from enum import Enum
from werkzeug.security import generate_password_hash

from shared.configs import *
from shared.utils import is_type_valid


class UserRoles(Enum):
    UR_ADMIN = 1
    UR_USER = 2
    UR_MAINTENANCE = 3

    def is_admin(self):
        return self == self.UR_ADMIN

    def is_user(self):
        return self == self.UR_USER

    def is_maintenance(self):
        return self == self.UR_MAINTENANCE

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class User:

    """
    User data container
    """

    def __init__(self, username, password,
                 user_id=None, user_role=None, is_text_password=False):

        self.user_id = user_id
        self.username = username
        self.password = password
        self.password_text = password
        self.user_role = self._get_user_role(user_role)

        if is_text_password:
            self.password = generate_password_hash(self.password)

    def can_add_users(self):
        if self.user_role.is_admin():
            return True

        return False

    def can_add_songs(self):
        if self.user_role.is_admin() or \
                self.user_role.is_maintenance():
            return True

        return False

    def _get_user_role(self, user_role):
        if user_role is None:
            return UserRoles.UR_USER

        if isinstance(user_role, UserRoles):
            return user_role
        
        # Invalid type input
        if not isinstance(user_role, int):
            return UserRoles.UR_USER

        # Input not present in available values
        if not UserRoles.has_value(user_role):
            # Default to user
            user_role = 2

        # If user-role value is provided
        return UserRoles(user_role)

    def is_valid(self):
        is_types_valid = all([
            is_type_valid(self.user_id, str),
            is_type_valid(self.username, str),
            is_type_valid(self.password, str),
            is_type_valid(self.user_role, UserRoles),
        ])
        if not is_types_valid:
            return False

        is_value_valid = all([
            MIN_USERNAME_LEN <= len(self.username) <= MAX_USERNAME_LEN,
            MIN_USERNAME_LEN <= len(self.password_text) <= MAX_USERNAME_LEN,
        ])
        return is_value_valid

    @staticmethod
    def from_json(data):

        if not isinstance(data, dict):
            return None

        try:
            return User(
                user_id=str(data['_id']),
                username=data['username'],
                password=data['password'],
                user_role=UserRoles(data['user_role']).value,
            )
        except KeyError:
            pass

        return None

    def to_json(self):
        cls_vars = vars(self)
        data = {k: v for k, v in cls_vars.items() if k not in ['user_role', 'user_id']}
        _id = {'_id': self.user_id} if self.user_id else {}

        return {**{'user_role': self.user_role.value}, **_id, **data}

    def __repr__(self):
        return f'name: {self.username}, role: {self.user_role}'
