import time
import functools
from flask import abort
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request

from song_server.shared.errorcodes import *
from song_server.models.user import User


"""
Decorators used throughout the application
"""


def body_sanity_check(keys_list=None):
    """
    A decorator to parse the request body and
    Ensure all required keys are available

    :param keys_list: A list of all required keys in the request body
    """

    if keys_list is None:
        keys_list = []

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            body = request.get_json()

            # Missing body
            if body is None and keys_list is not []:
                abort(400, INVALID_DATA_FORMAT)

            # Missing key
            if any([k not in body.keys() for k in keys_list]):
                abort(400, INVALID_DATA_FORMAT)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def parse_user(func):
    """
    Decorator around a request,
    Parses the user that made the request,
        - Ensures the user parsing is successful
        - Saves the user as a function attribute before returning

    User can be accessed using `func.user`
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Ensure the request has a session token
        # No jwt => no user data to parse
        verify_jwt_in_request()

        wrapper.user = User.from_json(get_jwt_identity())
        if wrapper.user is None:
            abort(400, USER_PARSE_ERROR)

        return func(*args, **kwargs)

    return wrapper


def timer(func):
    """
    Decorator,
    Prints the time taken for a function to execute
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_ts = time.perf_counter()
        ret = func(*args, **kwargs)
        time_elapsed_sec = time.perf_counter() - start_ts
        print('Timer Result, Func: ', func.__name__, ':', time_elapsed_sec, 'sec')

        return ret

    return wrapper
