from shared.configs import *
from shared.utils import is_type_valid


class Song:

    """
    Song data container
    """

    def __init__(self, name, cover_url, source_url,
                 is_explicit=False, times_played=0, num_likes=0, song_id=None):

        self.song_id = song_id
        self.name = name
        self.cover_url = cover_url
        self.source_url = source_url
        self.is_explicit = is_explicit
        self.times_played = times_played
        self.num_likes = num_likes

    def is_valid(self):

        # Data types validation
        is_types_valid = all([
            is_type_valid(self.song_id, str),
            is_type_valid(self.name, str),
            is_type_valid(self.cover_url, str),
            is_type_valid(self.source_url, str),
            is_type_valid(self.is_explicit, bool),
            is_type_valid(self.times_played, int),
            is_type_valid(self.num_likes, int),
        ])
        if not is_types_valid:
            return False

        # Value validation
        is_value_valid = all([
            MIN_SONG_NAME_LEN <= len(self.name) <= MAX_SONG_NAME_LEN,
            MIN_URL_LENGTH <= len(self.cover_url) <= MAX_URL_LENGTH,
            MIN_URL_LENGTH <= len(self.source_url) <= MAX_URL_LENGTH,
            self.times_played >= 0,
            self.num_likes >= 0
        ])

        return is_value_valid

    @staticmethod
    def from_json(data):
        try:
            return Song(
                song_id=str(data['_id']),
                name=data['name'],
                cover_url=data['cover_url'],
                source_url=data['source_url'],
                is_explicit=data['is_explicit'],
                times_played=data['times_played'],
                num_likes=data['num_likes'])
        except KeyError:
            pass

        return None

    def to_json(self):
        cls_vars = vars(self)
        data = {k: v for k, v in cls_vars.items() if k != 'song_id'}
        _id = {'_id': self.song_id} if self.song_id else {}

        return {**_id, **data}

    def __repr__(self):
        return f"name: {self.name}, likes: {self.num_likes}, played: {self.times_played}"
