import pytest

from shared.errorcodes import *
from shared.utils import remove_none_keys


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
        ('admin', 'admin', 200, SUCCESS),
        # Invalid admin login
        ('admin1', 'admin', 401, SIGN_IN_FAILURE),
        # Invalid password
        ('admin', '12345', 401, SIGN_IN_FAILURE),

        # User doesn't exist
        ('random_user', '12345', 401, SIGN_IN_FAILURE),
        # Valid user login
        ('Barbara Rocha', 'password', 200, SUCCESS),
        # Invalid user login
        ('Barbara Rocha', '12345678', 401, SIGN_IN_FAILURE),

        # TODO, add different data types data, and different length of data
        # ('abc'*1000, 'password'*1000)
        # (100, {'one': 1})
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

    if request.status_code == 200:
        # Valid request,
        # Ensure that the response has a access key
        body = request.get_json()
        assert 'access_key' in body
        assert len(body.get('access_key')) > 0

        # Return the access key for use in other tests
        return body.get('access_key')


@pytest.mark.parametrize(
    "request_username, request_password, "
    "username, password, dob, expected_code, return_code",
    [
        # Invalid login
        # Leads to failure in generation of access_key
        # then leads to jwt failure when adding new user
        (None, None, None, None, None, 401, SUCCESS),
        ('admin', 'wrong_password', None, None, None, 401, SUCCESS),
        ('wrong_username', 'wrong_password', None, None, None, 401, SUCCESS),
        ('admin', 'wrong_password', 'new_user', 'password', 12345, 401, SUCCESS),

        # Valid admin login and access key generation
        # Invalid body request
        # 1. No body
        ('admin', 'admin', None, None, None, 400, INVALID_DATA_FORMAT),
        # 2. No username key
        ('admin', 'admin', None, 'password', 12345, 400, INVALID_DATA_FORMAT),
        # 3. No password key
        ('admin', 'admin', 'new_user', None, 12345, 400, INVALID_DATA_FORMAT),
        # 4. No dob key
        ('admin', 'admin', 'new_user', 'password', None, 400, INVALID_DATA_FORMAT),

        # Valid admin login and access key generation
        # Invalid user details
        ('admin', 'admin', '', '', '', 400, INVALID_USER_DETAILS),
        ('admin', 'admin', '', 'password', 12345, 400, INVALID_USER_DETAILS),
        ('admin', 'admin', 'a', 'b', 12345, 400, INVALID_USER_DETAILS),
        ('admin', 'admin', 'abc', 'abc', 12345, 400, INVALID_USER_DETAILS),

        # Duplicate user
        ('admin', 'admin', 'Donald Lee', 'password', 12345, 400, USERNAME_EXISTS),

        # Valid request, admin adding a new user
        ('admin', 'admin', 'new_user', 'password', 12345, 200, SUCCESS),

        # Invalid request, non admin trying to add a new user
        ('Barbara Rocha', 'password', 'new_user', 'password', 12345, 400, PRIVILEGE_ERROR),
        ('Barbara Rocha', 'wrong_password', 'new_user', 'password', 12345, 401, SUCCESS),

        # TODO, add different data types data, and different length of data
    ]
)
def test_add_new_user(app, request_username, request_password,
                      username, password, dob, expected_code, return_code):

    # Make the login request with assertion disabled
    access_key = test_user_login(
        app, request_username, request_password,
        SUCCESS, SUCCESS, is_ignore_assertion=True)

    # Make request to add new user
    headers = None
    if access_key is not None:
        headers = {'Authorization': f'Bearer {access_key}'}
    body = {'username': username, 'password': password, 'dob': dob}
    body = remove_none_keys(body)
    request = app.post('/add_user', json=body, headers=headers)

    assert request is not None
    assert request.get_json() is not None
    assert request.status_code == expected_code

    # Process request return code
    request_code = request.get_json().get('code') or 0
    assert request_code == return_code
    if request.status_code != 200:
        return

    # If a new user was added clean up the user
    from extensions.dbhelper import db_helper
    db_helper.remove_user(username)
