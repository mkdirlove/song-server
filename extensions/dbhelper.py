import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash

from shared.configs import *
from shared.errorcodes import *
from models.user import User
from models.song import Song
from models.user import UserRoles


class DbHelper:

    def __init__(self, is_testing=False):
        self.is_testing = is_testing

        mongo_client = MongoClient(MONGO_DB_URL)
        db = mongo_client[TEST_MONGO_DB_NAME if is_testing else MONGO_DB_NAME]

        self.col_songs = db['songs']
        self.col_users = db['users']

        # Set unique keys
        self.col_users.create_index(
            [("username", pymongo.ASCENDING)], unique=True)
        self.col_songs.create_index(
            [("name", pymongo.ASCENDING),
             ("source_url", pymongo.ASCENDING)], unique=True)

    @staticmethod
    def _execute_query(collection, find_query, sort_by, page_number=1):
        return list(collection.find(find_query).sort(sort_by)\
            .skip((page_number - 1) * DB_ENTRIES_PER_PAGE)\
            .limit(DB_ENTRIES_PER_PAGE))

    def add_item(self, item):
        if item is None:
            return REQUEST_PARSE_ERROR

        is_song = isinstance(item, Song)
        is_user = isinstance(item, User)

        try:
            if is_song:
                self.col_songs.insert_one(item.to_json())
                return SUCCESS
            if is_user:
                self.col_users.insert_one(item.to_json())
                return SUCCESS
        except DuplicateKeyError:
            if is_user:
                return USERNAME_EXISTS
            if is_song:
                return SONG_EXISTS

            return DB_OPERATION_FAILURE
        except:
            return DB_OPERATION_FAILURE

        return REQUEST_PARSE_ERROR

    """
    Songs Db
    """

    def get_songs(self, page_number=1, explicit_query=False):

        explicit_query = {'is_explicit': {'$ne': True}} if explicit_query else {}
        find_query = {**explicit_query}

        return self._execute_query(
            collection=self.col_songs,
            find_query=find_query,
            sort_by='name',
            page_number=page_number
        )

    def remove_song(self, song_name):
        self.col_songs.delete_one({'name': song_name})

    """
    Users Db
    """

    def get_users(self, is_admin_only=False):
        find_query = {'user_role': UserRoles.UR_ADMIN.value} \
            if is_admin_only else {}

        return self._execute_query(
            collection=self.col_users,
            find_query=find_query,
            sort_by='username',
            page_number=1
        )

    def login_user(self, username, password):
        user = self.col_users.find_one({'username': username})
        user = User.from_json(user or {})

        # Error parsing user data or user doesn't exist
        if user is None:
            return

        # Password mismatch
        if not check_password_hash(user.password, password):
            return

        return user

    def remove_user(self, username):
        self.col_users.delete_one({'username':username})

    """
    Utils
    """

    def drop_all_collections(self):
        self.col_users.drop()
        self.col_songs.drop()


def init_db(is_testing=False):
    global db_helper
    db_helper = DbHelper(is_testing)


db_helper = None
