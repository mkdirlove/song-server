import os
import sys
import json
from pymongo import MongoClient

# Make song_server accessible for tests
song_server_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, song_server_dir)


class DbPopulate:

    def __init__(self, source_url, db_name):
        mongo_client = MongoClient(source_url)
        self.db = mongo_client[db_name]

    def load_test_data(self):

        # Drop all existing data
        self.db['songs'].drop()
        self.db['users'].drop()

        # Init data containers
        from song_server.shared.configs import DATA_FILE_SONGS
        from song_server.shared.configs import DATA_FILE_USERS
        songs = self._file_to_json(DATA_FILE_SONGS)
        users = self._file_to_json(DATA_FILE_USERS)

        # Repopulate db with test data
        self._db_dump_data('songs', songs)
        self._db_dump_data('users', users)

        # Convert json data to model objects
        from song_server.models.song import Song
        from song_server.models.user import User
        songs = [Song.from_json(s) for s in songs]
        users = [User.from_json(u) for u in users]

        return songs, users

    def _db_dump_data(self, collection_name, data):
        self.db[collection_name].insert_many(data)

    @staticmethod
    def _file_to_json(filepath):
        with open(filepath) as f:
            return json.load(f)


