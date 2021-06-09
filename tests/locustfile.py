import os
import sys
import locust
import random

from tests.dbpopulate import DbPopulate

# Make song_server accessible for swarm tests
song_server_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, song_server_dir)


"""
Locust Quickstart: https://docs.locust.io/en/stable/quickstart.html
Locust Docs: https://docs.locust.io/en/stable/writing-a-locustfile.html
"""


"""
Pre-Test Setup
"""

# Users
g_users = []
g_admins = []
g_maintainers = []

# Init Db, Init test data
from song_server.shared.configs import DevConfig
db_populate = DbPopulate(DevConfig.DB_SOURCE_URL, DevConfig.DB_NAME)
_songs, _users = db_populate.load_test_data()
for u in _users:
    if u.user_role.is_admin():
        g_admins.append((u.username, "admin"))
    if u.user_role.is_maintenance():
        g_maintainers.append((u.username, "password"))
    if u.user_role.is_user():
        g_users.append((u.username, "password"))


"""
Common Tasks
"""


def login_user(user):
    if not isinstance(user, ClientUser):
        return

    headers = {
        "username": user.username,
        "password": user.password
    }

    # Login, return the access key for the user
    response = user.client.post("login", headers=headers)
    return response.json().get('access_key')


def get_all_songs(user):
    if not isinstance(user, ClientUser):
        return

    body = {}
    user.client.get("get_songs", json=body)


def like_song(user):
    if not isinstance(user, ClientUser):
        return

    body = {"song_id": "3"}
    headers = {'Authorization': f'Bearer {user.access_token}'}
    user.client.post("like_song", json=body, headers=headers)


def play_song(user):
    if not isinstance(user, ClientUser):
        return

    body = {"song_id": "3"}
    headers = {'Authorization': f'Bearer {user.access_token}'}
    user.client.post("play_song", json=body, headers=headers)


"""
Locust Users
"""


class ClientUser(locust.HttpUser):
    weight = 10
    wait_time = locust.between(0.5, 2)
    tasks = {play_song: 5, like_song: 1, get_all_songs: 3}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = None
        self.password = None
        self.access_token = None

    def on_start(self):
        self.username, self.password = random.choice(g_users)
        self.access_token = login_user(self)


# class MaintenanceUser(HttpUser):
#     weight = 3
#     wait_time = between(3, 5)
#
#     def on_start(self):
#         random_user = random.choice(CLIENT_USERS)
#         body = dict(username=random_user[0], password=random_user[1])
#         self.client.post("/login", json=body)
#
#
# class AdminUser(HttpUser):
tasks = {like_song: 1}
#     weight = 1
#     wait_time = between(5, 10)
#
#     def on_start(self):
#         random_user = random.choice(CLIENT_USERS)
#         body = dict(username=random_user[0], password=random_user[1])
#         self.client.post("/login", json=body)
