from flask import abort
from flask import request
from flask import jsonify
from flask import Blueprint

from shared.errorcodes import *
from shared.utils import parse_json
from shared.decorators import body_sanity_check
from shared.decorators import parse_user
from extensions.dbhelper import db_helper
from models.song import Song

bp_songs = Blueprint('songs', __name__)


@bp_songs.route('/get_songs')
def get_all_songs():

    # Process query filters if any
    body = request.get_json() or {}
    is_filter_explicit = body.get('is_filter_explicit') or False
    page_number = body.get('page_number') or 1

    if page_number <= 0:
        abort(400, INVALID_DATA_FORMAT)

    data = db_helper.get_songs(
        page_number, is_filter_explicit)
    return jsonify({'data': parse_json(data)}), 200


@bp_songs.route('/add_song', methods=['POST'])
@parse_user
@body_sanity_check(['name', 'cover_url', 'source_url', 'release_date'])
def add_new_song():

    # Confirm if the user can add songs
    if not add_new_song.user.can_add_songs():
        abort(400, PRIVILEGE_ERROR)

    body = request.get_json()
    name = body['name']
    cover_url = body['cover_url']
    source_url = body['source_url']
    release_date = body['release_date']
    is_explicit = body.get('is_explicit') or False

    # Create a new song
    new_song = Song(name, cover_url, source_url,
                    release_date, is_explicit=is_explicit)
    ret = db_helper.add_item(new_song)
    if ret != SUCCESS:
        abort(400, ret)

    return jsonify({"message": "New song added"}), 200
