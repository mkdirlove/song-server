from flask import abort
from flask import request
from flask import jsonify
from flask import Blueprint
from flask_jwt_extended import create_access_token

from shared.errorcodes import *
from shared.configs import *
from shared.utils import is_type_valid
from shared.decorators import body_sanity_check
from shared.decorators import parse_user
from extensions.dbhelper import db_helper
from models.user import User


bp_user = Blueprint('user', __name__)


@bp_user.route('/login', methods=['POST'])
def user_login():

    headers = request.headers or {}
    username = headers.get('username')
    password = headers.get('password')
    if username is None or password is None:
        abort(400, INVALID_DATA_FORMAT)

    # Type checks
    if not is_type_valid(username, str):
        abort(400, INVALID_DATA_FORMAT)
    if not is_type_valid(password, str):
        abort(400, INVALID_DATA_FORMAT)

    # Length checks
    if 0 >= len(username) >= MAX_USERNAME_LEN:
        abort(400, SIGN_IN_FAILURE)
    if 0 >= len(password) >= MAX_PASSWORD_LEN:
        abort(400, SIGN_IN_FAILURE)

    user = db_helper.login_user(username, password)
    if not user:
        abort(401, SIGN_IN_FAILURE)

    access_key = create_access_token(user.to_json())
    ret = {
        "message": "successful login",
        "access_key": access_key
    }
    return jsonify(ret), 201


@bp_user.route('/add_user', methods=['POST'])
@parse_user
@body_sanity_check(['username', 'password'])
def add_new_user():

    if not add_new_user.user.can_add_users():
        abort(400, PRIVILEGE_ERROR)

    body = request.get_json()
    username = body['username']
    password = body['password']

    # Create a new user
    new_user = User(username, password, is_text_password=True)
    if not new_user.is_valid():
        abort(400, INVALID_USER_DETAILS)

    ret = db_helper.add_item(new_user)
    if ret != SUCCESS:
        # User addition failed
        abort(400, ret)

    return jsonify({"message": "New user added"}), 201
