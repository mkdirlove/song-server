import os


"""
Default App Configurations
"""

# Songs Configs
MIN_SONG_NAME_LEN = 5
MAX_SONG_NAME_LEN = 100
MIN_URL_LENGTH = 3
MAX_URL_LENGTH = 100
MAX_SONG_ID_LEN = 20

# User Configs
MIN_USERNAME_LEN = 5
MAX_USERNAME_LEN = 100
MIN_PASSWORD_LEN = 5
MAX_PASSWORD_LEN = 100

# Db populate
NUM_SONGS = 2500
NUM_USERS = 250
COMMON_USER_PASSWORD = 'password'

# DB Configs
DB_ENTRIES_PER_PAGE = 25

# Tests
DATA_FILE_SONGS = 'tests/data/songs.json'
DATA_FILE_USERS = 'tests/data/users.json'


"""
Flask Configs
"""


class DefaultConfig:

    # Flask Configs
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(24)
    SESSION_COOKIE_SECURE = True

    # DB Configs
    DB_SOURCE_URL = 'mongodb://localhost:27017'
    DB_NAME = 'songs_db'


class DevConfig(DefaultConfig):
    DEBUG = True


class TestConfig(DefaultConfig):
    TESTING = True
    DB_NAME = 'songs_db_test'
