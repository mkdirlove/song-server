
class Song:

    def __init__(self, name, cover_url, source_url, release_date,
                 is_explicit=False, times_played=0, num_likes=0, song_id=None):

        self.song_id = song_id
        self.name = name
        self.cover_url = cover_url
        self.source_url = source_url
        self.release_date = release_date
        self.is_explicit = is_explicit
        self.times_played = times_played
        self.num_likes = num_likes

    @staticmethod
    def from_json(data):
        try:
            return Song(
                song_id=str(data['_id']),
                name=data['name'],
                cover_url=data['cover_url'],
                source_url=data['source_url'],
                release_date=data['release_date'],
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

    def __str__(self):
        return f"name: {self.name}, likes: {self.num_likes}, played: {self.times_played}"
