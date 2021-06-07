# App Configurations

# General
IS_DEBUG_MODE = True

# DB Configs
MONGO_DB_URL = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'songs_db'
DB_ENTRIES_PER_PAGE = 25

# Songs Configs
MIN_SONG_NAME_LEN = 5
MAX_SONG_NAME_LEN = 100
MIN_URL_LENGTH = 3
MAX_URL_LENGTH = 100

# User Configs
MIN_USERNAME_LEN = 5
MAX_USERNAME_LEN = 100
MIN_PASSWORD_LEN = 5
MAX_PASSWORD_LEN = 100

# Db populate
NUM_SONGS = 2500
NUM_USERS = 250
COMMON_USER_PASSWORD = 'password'

# Tests
TEST_MONGO_DB_NAME = 'songs_db_test'
DATA_FILE_SONGS = 'data/songs.json'
DATA_FILE_USERS = 'data/users.json'
