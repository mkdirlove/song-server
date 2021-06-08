import pytest

from song_server.shared.errorcodes import *
from song_server.shared.utils import remove_none_keys


"""
Tests for users blueprint,
Located at song_server/services/users
"""


@pytest.mark.parametrize(
    "username, password, expected_code, return_code",
    [
        # Data none, leads to empty headers
        (None, None, 400, INVALID_DATA_FORMAT),
        # Username none
        (None, 'password', 400, INVALID_DATA_FORMAT),
        # Password none
        ('username', None, 400, INVALID_DATA_FORMAT),
        # Null string headers
        ('', '', 401, SIGN_IN_FAILURE),

        # Valid admin login
        ('admin', 'admin', 201, SUCCESS),
        # Invalid admin login
        ('admin1', 'admin', 401, SIGN_IN_FAILURE),
        # Invalid password
        ('admin', '12345', 401, SIGN_IN_FAILURE),

        # Maintenance login
        ('Patrick Smith', 'password', 201, SUCCESS),
        ('Patrick Smith', 'wrong-pass', 401, SIGN_IN_FAILURE),
        ('Patrick A Smith', 'password', 401, SIGN_IN_FAILURE),

        # User doesn't exist
        ('random_user', '12345', 401, SIGN_IN_FAILURE),
        # Valid user login
        ('Barbara Rocha', 'password', 201, SUCCESS),
        # Invalid user login
        ('Barbara Rocha', '12345678', 401, SIGN_IN_FAILURE),

        # Invalid data, either types or len
        ('abc'*1000, 'password', 401, SIGN_IN_FAILURE),
        ('abcdef', 'password'*1000, 401, SIGN_IN_FAILURE),
        # (100, 'password', 400, INVALID_DATA_FORMAT),
        # ('abcdef', {'one': 1}, 400, INVALID_DATA_FORMAT),
    ]
)
def test_user_login(app, username, password,
                    expected_code, return_code, is_ignore_assertion=False):

    # Make the login request
    headers = {'username': username, 'password': password}
    headers = remove_none_keys(headers)
    request = app.post('/login', headers=headers)

    assert request is not None
    assert request.get_json() is not None

    if not is_ignore_assertion:
        assert request.status_code == expected_code

        # Process request return code
        # 0 => SUCCESS
        request_return_code = request.get_json().get('code') or 0
        assert request_return_code == return_code

    if request.status_code == 201:
        # Valid request,
        # Ensure that the response has a access key
        body = request.get_json()
        assert 'access_key' in body
        assert len(body.get('access_key')) > 0

        # Return the access key for use in other tests
        return body.get('access_key')


@pytest.mark.parametrize(
    "request_username, request_password, "
    "username, password, expected_code, return_code",
    [
        # Invalid login
        # Leads to failure in generation of access_key
        # then leads to jwt failure when adding new user
        (None, None, None, None, 401, SUCCESS),
        ('admin', 'wrong_password', None, None, 401, SUCCESS),
        ('wrong_username', 'wrong_password', None, None, 401, SUCCESS),
        ('admin', 'wrong_password', 'new_user', 'password', 401, SUCCESS),

        # Valid admin login and access key generation
        # Invalid body request
        # 1. No body
        ('admin', 'admin', None, None, 400, INVALID_DATA_FORMAT),
        # 2. No username key
        ('admin', 'admin', None, 'password', 400, INVALID_DATA_FORMAT),
        # 3. No password key
        ('admin', 'admin', 'new_user', None, 400, INVALID_DATA_FORMAT),

        # Valid admin login and access key generation
        # Invalid user details
        ('admin', 'admin', '', '', 400, INVALID_USER_DETAILS),
        ('admin', 'admin', '', 'password', 400, INVALID_USER_DETAILS),
        ('admin', 'admin', 'a', 'b', 400, INVALID_USER_DETAILS),
        ('admin', 'admin', 'abc', 'abc', 400, INVALID_USER_DETAILS),

        # Maintenance users can't add new users
        ('Patrick Smith', 'password', 'new_user', 'password', 400, PRIVILEGE_ERROR),
        ('Patrick Smith', 'wrong-password', 'new_user', 'password', 401, SUCCESS),

        # Duplicate user
        ('admin', 'admin', 'Donald Lee', 'password', 400, USERNAME_EXISTS),

        # Valid request, admin adding a new user
        ('admin', 'admin', 'new_user', 'password', 201, SUCCESS),

        # Invalid request, non-admin trying to add a new user
        ('Barbara Rocha', 'password', 'new_user', 'password', 400, PRIVILEGE_ERROR),
        ('Barbara Rocha', 'wrong-password', 'new_user', 'password', 401, SUCCESS),

        # Invalid data types or invalid length
        ('admin', 'admin', ['item'], 'password', 400, INVALID_USER_DETAILS),
        ('admin', 'admin', 'new-user', 1000, 400, INVALID_USER_DETAILS),
        ('admin', 'admin', 'new_user'*100, 'password', 400, INVALID_USER_DETAILS),
        ('admin', 'admin', 'new_user', 'password'*100, 400, INVALID_USER_DETAILS),
    ]
)
def test_add_new_user(app, request_username, request_password,
                      username, password, expected_code, return_code):

    # Make the login request with assertion disabled
    access_token = test_user_login(
        app, request_username, request_password,
        SUCCESS, SUCCESS, is_ignore_assertion=True)

    # Make request to add new user
    headers = None
    if access_token is not None:
        headers = {'Authorization': f'Bearer {access_token}'}
    body = {'username': username, 'password': password}
    body = remove_none_keys(body)
    request = app.post('/add_user', json=body, headers=headers)

    assert request is not None
    assert request.get_json() is not None
    assert request.status_code == expected_code

    # Process request return code
    request_code = request.get_json().get('code') or 0
    assert request_code == return_code
    if request.status_code != 201:
        return

    # If a new user was added clean up the user
    from song_server.extensions.dbhelper import db_helper
    db_helper.remove_user(username)
