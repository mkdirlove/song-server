# App Configurations

# General
IS_DEBUG_MODE = True

# DB Configs
MONGO_DB_URL = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'songs_db'
DB_ENTRIES_PER_PAGE = 25

# Db populate
NUM_SONGS = 2500
NUM_USERS = 250
COMMON_USER_PASSWORD = 'password'

# Tests
TEST_MONGO_DB_NAME = 'songs_db_test'
DATA_FILE_SONGS = 'data/songs.json'
DATA_FILE_USERS = 'data/users.json'
