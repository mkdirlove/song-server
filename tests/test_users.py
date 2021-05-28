import pytest
from werkzeug.security import check_password_hash

from shared.configs import *
from shared.utils import remove_none_keys
from shared.utils import search_users_list


@pytest.mark.parametrize(
    "username, password, expected_code",
    [
        ('username', None, 400),             # Password none
        (None, 'password', 400),             # Username none
        (None, None, 400),                   # Data none, leads to empty headers
        ('', '', 401),                       # Empty headers

        ('admin', 'admin', 200),             # Valid admin login
        ('admin1', 'admin', 401),            # Invalid admin login
        ('admin', '12345', 401),             # Invalid password

        ('random_user', '12345', 401),       # User doesn't exist
        ('Barbara Rocha', 'password', 200),  # Valid user login
        ('Barbara Rocha', '12345678', 401),  # Invalid user login

        # TODO, add different data types data, and different length of data
        # ('abc'*1000, 'password'*1000)
        # (100, {'one': 1})
    ]
)
def test_user_login(app, username, password,
                    expected_code, is_ignore_assertion=False):

    # Make the login request
    headers = {'username': username, 'password': password}
    headers = remove_none_keys(headers)
    request = app.post('/login', headers=headers)

    if not is_ignore_assertion:
        assert request.status_code == expected_code
    if request.status_code == 200:
        # Valid request,
        # Ensure that the response has a access key
        body = request.get_json()
        assert 'access_key' in body
        assert len(body.get('access_key')) > 0

        # Return the access key for use in other tests
        return body.get('access_key')


@pytest.mark.parametrize(
    "request_username, request_password, username, password, dob, expected_code",
    [
        # Invalid login
        # Leads to failure in generation of access_key
        # then leads to jwt failure when adding new user
        (None, None, None, None, None, 401),
        ('admin', 'wrong_password', None, None, None, 401),
        ('wrong_username', 'wrong_password', None, None, None, 401),
        ('admin', 'wrong_password', 'new_user', 'password', 12345, 401),

        # Valid admin login and access key generation
        # Invalid body request
        ('admin', 'admin', None, None, None, 400),               # No body
        ('admin', 'admin', None, 'password', 12345, 400),        # No username key
        ('admin', 'admin', 'new_user', None, 12345, 400),        # No password key
        ('admin', 'admin', 'new_user', 'password', None, 400),   # No dob key

        # Valid admin login and access key generation
        # Invalid user details
        ('admin', 'admin', '', '', '', 400),
        ('admin', 'admin', '', 'password', 12345, 400),
        ('admin', 'admin', 'a', 'b', 12345, 400),
        ('admin', 'admin', 'abc', 'abc', 12345, 400),

        # Duplicate user
        ('admin', 'admin', 'Donald Lee', 'password', 12345, 400),

        # Valid request, admin adding a new user
        ('admin', 'admin', 'new_user', 'password', 12345, 200),

        # Invalid request, non admin trying to add a new user
        ('Barbara Rocha', 'password', 'new_user', 'password', 12345, 400),
        ('Barbara Rocha', 'wrong_password', 'new_user', 'password', 12345, 401),

        # TODO, add different data types data, and different length of data
    ]
)
def test_add_new_user(app, request_username, request_password,
                      username, password, dob, expected_code):

    # Make the login request
    access_key = test_user_login(
        app, request_username, request_password,
        expected_code, is_ignore_assertion=True)

    # Make request to add new user
    headers = None
    if access_key is not None:
        headers = {'Authorization': f'Bearer {access_key}'}
    body = {'username': username, 'password': password, 'dob': dob}
    body = remove_none_keys(body)
    request = app.post('/add_user', json=body, headers=headers)

    assert request.status_code == expected_code
    if request.status_code != 200:
        return

    # If a new user was added clean up the user
    from extensions.dbhelper import db_helper
    db_helper.remove_user(username)
