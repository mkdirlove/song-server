import os
import sys
import pytest

# Make song_server accessible for tests
song_server_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, song_server_dir)

from tests.db.dbpopulate import DbPopulate
from song_server.shared.configs import *
from song_server.app import create_app


"""
Pytest Config file,
Houses all initializations and fixtures

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
Pre-Test Setup
"""

# Init Db, Init test data
db_populate = DbPopulate(TestConfig.DB_SOURCE_URL, TestConfig.DB_NAME)
_songs, _users = db_populate.load_test_data()
