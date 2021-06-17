import os
import random
import sys
import json
from faker import Faker
from pymongo import MongoClient

# Make song_server accessible for tests
song_server_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, song_server_dir)

from song_server.shared.configs import DATA_FILE_SONGS
from song_server.shared.configs import DATA_FILE_USERS
from song_server.models.song import Song
from song_server.models.user import User


"""
Module responsible for populating fake data to db
Faker docs - https://faker.readthedocs.io/en/master/
"""


class DbPopulate:

    def __init__(self, source_url, db_name):
        mongo_client = MongoClient(source_url)

        self.db = mongo_client[db_name]
        self.faker = Faker()

    def load_test_data(self):

        # Drop all existing data
        self.db['songs'].drop()
        self.db['users'].drop()

        # Init data containers
        songs = self._file_to_json(DATA_FILE_SONGS)
        users = self._file_to_json(DATA_FILE_USERS)

        # Repopulate db with test data
        self._db_dump_data('songs', songs)
        self._db_dump_data('users', users)

        # Convert json data to model objects
        songs = [Song.from_json(s) for s in songs]
        users = [User.from_json(u) for u in users]

        return songs, users

    def get_rand_int(self, max_value=9999):
        return self.faker.pyint(
            min_value=10, max_value=max_value)

    def get_random_song(self):
        return Song(
            name=self.faker.sentence(),
            cover_url=self.faker.img_url(),
            source_url=f'www.song_server.com/{self.get_rand_int()}',
            is_explicit=bool(random.getrandbits(1))
        )

    def _db_dump_data(self, collection_name, data):
        self.db[collection_name].insert_many(data)

    @staticmethod
    def _file_to_json(filepath):
        with open(filepath) as f:
            return json.load(f)


