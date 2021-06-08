import pytest

from song_server.shared.errorcodes import *
from song_server.shared.configs import *
from song_server.shared.utils import remove_none_keys


"""
Tests for songs blueprint,
Located at song_server/services/songs
"""


@pytest.mark.parametrize(
    "is_filter_explicit, page_number, expected_code, return_code",
    [
        # None data
        (None, None, 201, SUCCESS),
        (True, None, 201, SUCCESS),
        # 0 page-number gets converted to 1
        (None, 0, 201, SUCCESS),

        # page-number
        (None, -1, 400, INVALID_DATA_FORMAT),
        (None, -999, 400, INVALID_DATA_FORMAT),
        (None, 1, 201, SUCCESS),
        (None, 99999, 201, SUCCESS),

        # is-filter-explicit
        (True, 1, 201, SUCCESS),
        (False, 1, 201, SUCCESS),

        # Invalid data types
        (100, "wrong-data", 400, INVALID_DATA_FORMAT),
        (True, "wrong-data", 400, INVALID_DATA_FORMAT),
        ("wrong-data", 1, 400, INVALID_DATA_FORMAT),
    ]
)
def test_get_all_songs(app, songs_data, is_filter_explicit, page_number,
                       expected_code, return_code):

    body = {
        'is_filter_explicit': is_filter_explicit,
        'page_number': page_number
    }
    body = remove_none_keys(body)
    request = app.get('/get_songs', json=body)

    assert request is not None
    assert request.get_json() is not None

    request_return_code = request.get_json().get('code') or 0
    assert request_return_code == return_code
    assert request.status_code == expected_code

    if request.status_code == 201:

        # default transformations within request
        is_filter_explicit = is_filter_explicit or False
        page_number = page_number or 1

        expected_data = [s.to_json() for s in songs_data
                         if not s.is_explicit or not is_filter_explicit]
        expected_data.sort(key=lambda x: x['name'])
        start_index = (page_number - 1) * DB_ENTRIES_PER_PAGE
        expected_data = expected_data[
                        start_index:start_index+DB_ENTRIES_PER_PAGE]

        assert request.get_json() is not None
        assert 'data' in request.get_json()
        assert request.get_json() == dict(data=expected_data)


@pytest.mark.parametrize(
    "username, password, song_name, cover_url, "
    "source_url, is_explicit, expected_code, return_code",
    [
        # Invalid login
        # Jwt failure when adding new user
        (None, None, None, None, None, None, 401, SUCCESS),
        ('admin', 'wrong_password', None, None, None, None, 401, SUCCESS),
        ('wrong_username', 'wrong_password', None, None, None, None, 401, SUCCESS),
        ('admin', 'wrong_password', None, None, None, None, 401, SUCCESS),

        # Valid admin login, Invalid body
        # 1. No song-name
        ('admin', 'admin', None, 'url', 'url', True, 400, INVALID_DATA_FORMAT),
        # 2. No cover-url
        ('admin', 'admin', 'song-name', None, 'url', True, 400, INVALID_DATA_FORMAT),
        # 3. No source-url
        ('admin', 'admin', 'song-name', 'url', None, True, 400, INVALID_DATA_FORMAT),
        # 4. No explicit tag, defaults to False
        ('admin', 'admin', 'song-name', 'url', 'url', None, 201, SUCCESS),

        # Duplicate songs
        # 1. Same song-name and different source-url allowed
        ('admin', 'admin', 'Whatever put local society same.', 'url',
         'url', None, 201, SUCCESS),
        # 2. Same song-name and same source-url not allowed
        ('admin', 'admin', 'Whatever put local society same.', 'url',
         'www.song_server.com/2192', None, 400, SONG_EXISTS),
        # 3. cover-url immaterial
        ('admin', 'admin', 'Whatever put local society same.',
         'www.song_server.com/2192', 'url', None, 201, SUCCESS),

        # Invalid request, user trying to add a new song
        ('Barbara Rocha', 'password', 'new-song',
         'url', 'url', None, 400, PRIVILEGE_ERROR),
        ('Barbara Rocha', 'bad-password', 'new-song',
         'url', 'url', None, 401, SUCCESS),

        # Valid request, maintenance user adding a song
        ('Patrick Smith', 'password', 'new-song', 'url', 'url', True, 201, SUCCESS),
        ('Patrick Smith', 'wrong-password', 'new-song', 'url', 'url', True, 401, SUCCESS),
        ('Teresa Rodriguez', 'password', 'new-song', 'url', 'url', False, 201, SUCCESS),

        # Valid request, admin adding a new song
        ('admin', 'admin', 'new-song', 'url', 'url', True, 201, SUCCESS),
        ('admin', 'wrong-password', 'new-song', 'url', 'url', True, 401, SUCCESS),
        ('admin', 'admin', 'new-song', 'url', 'url', False, 201, SUCCESS),

        # Invalid data, either type or value
        ('admin', 'admin', 9921, 'url', 'url', False, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', {'a': 1}, 'url', False, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', 'url', ['item'], True, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', 'url', 'url', 100, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', {'a': 1}, ['item'], False, 400, INVALID_SONG_DETAILS),

        # Invalid data length
        ('admin', 'admin', '', 'url', 'url', True, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', '', 'url', True, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', 'url', '', True, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'song-name'*1000, 'url', 'url', True, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', 'url'*1000, 'url', True, 400, INVALID_SONG_DETAILS),
        ('admin', 'admin', 'new-song', 'url', 'url'*1000, True, 400, INVALID_SONG_DETAILS),
    ]
)
def test_add_new_song(app, username, password,
                      song_name, cover_url, source_url,
                      is_explicit, expected_code, return_code):

    # Login the user to obtain an access token
    headers = {'username': username, 'password': password}
    headers = remove_none_keys(headers)
    request = app.post('/login', headers=headers)

    assert request is not None
    assert request.get_json() is not None

    body = request.get_json() or {}
    access_token = body.get('access_key')

    # Request to add a new song
    headers = None
    if access_token is not None:
        headers = {'Authorization': f'Bearer {access_token}'}
    body = {
        'name': song_name,
        'cover_url': cover_url,
        'source_url': source_url,
        'is_explicit': is_explicit
    }
    body = remove_none_keys(body)
    request = app.post('/add_song', json=body, headers=headers)

    # Validate response
    assert request is not None
    assert request.get_json() is not None
    assert request.status_code == expected_code
    request_code = request.get_json().get('code') or 0

    assert request_code == return_code
    if request.status_code != 201:
        return

    # If a new song was added remove it
    from song_server.extensions.dbhelper import db_helper
    db_helper.remove_song(song_name, source_url)


@pytest.mark.parametrize(
    "username, password, song_id, "
    "expected_code, return_code",
    [
        # Invalid user login
        ("admin", "wrong-pass", "song-id", 401, SUCCESS),

        # Valid login, wrong song-id
        ("admin", "admin", "song-id", 400, SONG_NOT_FOUND),

        # Large song-id
        ("admin", "admin", "song-id"*100, 400, INVALID_SONG_DETAILS),

        # Valid login, valid song-id
        # Admin
        ("admin", "admin", "5", 201, SUCCESS),
        # Maintenance
        ("Patrick Smith", "password", "4", 201, SUCCESS),
        # User
        ("Barbara Rocha", "password", "3", 201, SUCCESS),
    ]
)
def test_like_song(app, username, password, song_id,
                   expected_code, return_code):

    # Login the user to obtain an access token
    headers = {'username': username, 'password': password}
    headers = remove_none_keys(headers)
    request = app.post('/login', headers=headers)

    assert request is not None
    assert request.get_json() is not None

    body = request.get_json() or {}
    access_token = body.get('access_key')

    # Request to like a song
    headers = None
    if access_token is not None:
        headers = {'Authorization': f'Bearer {access_token}'}
    body = dict(song_id=song_id)
    body = remove_none_keys(body)
    request = app.post('/like_song', json=body, headers=headers)

    # Validate response
    assert request is not None
    assert request.get_json() is not None
    assert request.status_code == expected_code

    request_code = request.get_json().get('code') or 0
    assert request_code == return_code


@pytest.mark.parametrize(
    "username, password, song_id, "
    "expected_code, return_code",
    [
        # Invalid user login
        ("admin", "wrong-pass", "song-id", 401, SUCCESS),

        # Valid login, wrong song-id
        ("admin", "admin", "song-id", 400, SONG_NOT_FOUND),

        # Large song-id
        ("admin", "admin", "song-id"*100, 400, INVALID_SONG_DETAILS),

        # Valid login, valid song-id
        # Admin
        ("admin", "admin", "5", 201, SUCCESS),
        # Maintenance
        ("Patrick Smith", "password", "4", 201, SUCCESS),
        # User
        ("Barbara Rocha", "password", "3", 201, SUCCESS),
    ]
)
def test_play_song(app, username, password, song_id,
                   expected_code, return_code):

    # Login the user to obtain an access token
    headers = {'username': username, 'password': password}
    headers = remove_none_keys(headers)
    request = app.post('/login', headers=headers)

    assert request is not None
    assert request.get_json() is not None

    body = request.get_json() or {}
    access_token = body.get('access_key')

    # Request to play a song
    headers = None
    if access_token is not None:
        headers = {'Authorization': f'Bearer {access_token}'}
    body = dict(song_id=song_id)
    body = remove_none_keys(body)
    request = app.post('/play_song', json=body, headers=headers)

    # Validate response
    assert request is not None
    assert request.get_json() is not None
    assert request.status_code == expected_code

    request_code = request.get_json().get('code') or 0
    assert request_code == return_code
