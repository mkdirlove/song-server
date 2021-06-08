from flask import abort
from flask import request
from flask import jsonify
from flask import Blueprint

from song_server.shared.errorcodes import *
from song_server.shared.configs import *
from song_server.shared.utils import parse_json
from song_server.shared.utils import is_type_valid
from song_server.shared.decorators import body_sanity_check
from song_server.shared.decorators import parse_user
from song_server.extensions.dbhelper import db_helper
from song_server.models.song import Song

bp_songs = Blueprint('songs', __name__)


"""
Songs Service
"""


@bp_songs.route('/get_songs')
def get_all_songs():
    """
    Return a list of all songs in the db paginated,
    Request type: GET, body optional

    Body Keys (optional),
    - is_filter_explicit: bool, False by default, filters explicit songs when True
    - page_number: int, 1 by default
    """

    # Process query filters if any
    body = request.get_json() or {}
    is_filter_explicit = body.get('is_filter_explicit') or False
    page_number = body.get('page_number') or 1

    # Type checks
    if not is_type_valid(is_filter_explicit, bool):
        abort(400, INVALID_DATA_FORMAT)
    if not is_type_valid(page_number, int):
        abort(400, INVALID_DATA_FORMAT)

    if page_number <= 0:
        abort(400, INVALID_DATA_FORMAT)

    data = db_helper.get_songs(
        page_number, is_filter_explicit)
    return jsonify({'data': parse_json(data)}), 201


@bp_songs.route('/add_song', methods=['POST'])
@parse_user
@body_sanity_check(['name', 'cover_url', 'source_url'])
def add_new_song():
    """
    Add a new song to the db
    Request type: POST

    Body Keys,
    - name: str, name of the new song, required
    - cover_url: str, song cover url, required
    - source_url: str, song source url, required
    - is_explicit: bool, True if song is explicit, False by default, optional
    """

    # Confirm if the user can add songs
    if not add_new_song.user.can_add_songs():
        abort(400, PRIVILEGE_ERROR)

    body = request.get_json()
    name = body['name']
    cover_url = body['cover_url']
    source_url = body['source_url']
    is_explicit = body.get('is_explicit') or False

    # Create a new song
    new_song = Song(name, cover_url, source_url, is_explicit=is_explicit)
    if not new_song.is_valid():
        abort(400, INVALID_SONG_DETAILS)

    ret = db_helper.add_item(new_song)
    if ret != SUCCESS:
        abort(400, ret)

    return jsonify({"message": "New song added"}), 201


@bp_songs.route('/like_song', methods=['POST'])
@parse_user
@body_sanity_check(['song_id'])
def like_song():
    """
    Like a specific song
    Request Type: POST

    Body Keys,
    - song_id: str, id of the song to be liked, required
    """

    body = request.get_json()
    song_id = body['song_id']

    if len(song_id) > MAX_SONG_ID_LEN:
        abort(400, INVALID_SONG_DETAILS)

    # Like song
    ret = db_helper.like_song(song_id)
    if ret != SUCCESS:
        abort(400, ret)

    return jsonify({"message": "Song liked"}), 201


@bp_songs.route('/play_song', methods=['POST'])
@parse_user
@body_sanity_check(['song_id'])
def play_song():
    """
    Play a specific song
    Request Type: POST

    Body Keys,
    - song_id: str, id of the song to be played, required
    """

    body = request.get_json()
    song_id = body['song_id']

    if len(song_id) > MAX_SONG_ID_LEN:
        abort(400, INVALID_SONG_DETAILS)

    # Play the requested song
    ret = db_helper.play_song(song_id)
    if ret != SUCCESS:
        abort(400, ret)

    return jsonify({"message": "Song played"}), 201
