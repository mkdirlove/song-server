import pytest
from werkzeug.security import check_password_hash


@pytest.mark.parametrize(
    "username, password",
    [
        ('username', None),             # Password none
        (None, 'password'),             # Username none
        (None, None),                   # Data none, leads to empty headers

        ('admin', 'admin'),             # Valid admin login
        ('admin', '12345'),             # Invalid password

        ('random_user', '12345'),       # User doesn't exist
        ('Barbara Rocha', '12345678'),  # Invalid user login
        ('Barbara Rocha', 'password'),  # Valid user login
    ]
)
def test_user_login(app, users_data, username, password):

    # Parse request headers
    headers = {}
    if username is not None:
        headers = {'username': username}
    if password is not None:
        headers = {**headers, **{'password': password}}

    # Make the login request
    request = app.post('/login', headers=headers)

    # Expected response
    expected_code = 200
    # Search if user exists
    user = next((item for item in users_data
                 if item.username == username), None)
    if user is None:
        expected_code = 401
    elif not check_password_hash(user.password, password):
        expected_code = 401

    if username is None or password is None:
        expected_code = 400

    assert request.status_code == expected_code
    if expected_code == 200:
        # Valid request,
        # Ensure that the response has a access key
        body = request.get_json()
        assert 'access_key' in body
        assert len(body.get('access_key')) > 0
