import pytest
from werkzeug.security import check_password_hash

from shared.utils import remove_none_keys


@pytest.mark.parametrize(
    "username, password",
    [
        ('username', None),             # Password none
        (None, 'password'),             # Username none
        (None, None),                   # Data none, leads to empty headers
        ('', ''),  # Empty headers

        ('admin', 'admin'),             # Valid admin login
        ('admin1', 'admin'),            # Invalid admin login
        ('admin', '12345'),             # Invalid password

        ('random_user', '12345'),       # User doesn't exist
        ('Barbara Rocha', 'password'),  # Valid user login
        ('Barbara Rocha', '12345678'),  # Invalid user login

        # TODO, add different data types data, and different length of data
        # ('abc'*1000, 'password'*1000)
        # (100, {'one': 1})
    ]
)
def test_user_login(app, users_data, username, password):

    # Make the login request
    headers = {'username': username, 'password': password}
    headers = remove_none_keys(headers)
    request = app.post('/login', headers=headers)

    # Expected response
    expected_code = 200
    # Search if user exists
    user = next((item for item in users_data
                 if item.username == username), None)
    if user is None or \
            not check_password_hash(user.password, password):
        expected_code = 401
    if username is None or password is None:
        expected_code = 400

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
    "request_username, request_password, username, password, dob",
    [
        # Invalid login
        (None, None, None, None, None),
        ('admin', 'wrong_password', 'new_user', 'password', 12345),
        ('wrong_username', 'wrong_password', 'new_user', 'password', 12345),

        ('admin', 'admin', 'new_user', 'password', 12345),
        ('admin', 'admin', 'new_user', 'password', 12345),
    ]
)
def test_add_new_user(app, users_data,
                      request_username, request_password,
                      username, password, dob):

    # Make the login request
    access_key = test_user_login(app, users_data,
                                 request_username, request_password)

    # Make request to add new user
    headers = None
    if access_key is not None:
        headers = {'Authorization': f'Bearer {access_key}'}
    body = {'username': username, 'password': password, 'dob': dob}
    body = remove_none_keys(body)
    request = app.post('/add_user', json=body, headers=headers)

    # Expected response
    expected_code = 200
    if headers is None:
        expected_code = 401

    user = next((item for item in users_data
                 if item.username == request_username), None)
    new_user = next((item for item in users_data
                 if item.username == username), None)
    if user is None:
        expected_code = 401
    elif user.can_add_users():
        expected_code = 400

    if new_user is not None:
        expected_code = 400

    assert request.status_code == expected_code
    if request.status_code != 200:
        return

    # If a new user was added clean up the user
    from extensions.dbhelper import db_helper
    db_helper.remove_user(username)
