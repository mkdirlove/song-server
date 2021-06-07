import json
import pytest
from pymongo import MongoClient

from song_server.shared.configs import *
from song_server.models.song import Song
from song_server.models.user import User
from song_server.app import create_app


"""
Pytest Docs - https://docs.pytest.org/en/6.2.x/
Pytest Fixtures - https://docs.pytest.org/en/6.2.x/fixture.html
Pytest Parameterized testing - https://docs.pytest.org/en/6.2.x/example/parametrize.html
Flask Testing Docs - https://flask.palletsprojects.com/en/2.0.x/testing/

pytest -v (verbose) -s (show print statements)
"""


@pytest.fixture
def app():
    flask_app = create_app(is_testing=True)

    # Return the flask test client
    yield flask_app.test_client()


@pytest.fixture
def songs_data():
    return _songs


@pytest.fixture
def users_data():
    return _users


"""
Testing Setup
"""


def _db_dump_data(collection_name, data):
    _db[collection_name].insert_many(data)


def _file_to_json(filepath):
    with open(filepath) as f:
        return json.load(f)


# Load test data
_mongo_client = MongoClient(MONGO_DB_URL)
_db = _mongo_client[TEST_MONGO_DB_NAME]

# Drop all existing data
_db['songs'].drop()
_db['users'].drop()

# Data containers
_songs = _file_to_json(DATA_FILE_SONGS)
_users = _file_to_json(DATA_FILE_USERS)

# Repopulate db with test data
_db_dump_data('songs', _songs)
_db_dump_data('users', _users)

# Convert json data to model objects
_songs = [Song.from_json(s) for s in _songs]
_users = [User.from_json(u) for u in _users]
