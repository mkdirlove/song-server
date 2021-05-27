from flask_jwt_extended import JWTManager

from shared.utils import get_secret_key


"""
Flask-JWT-Extended docs - https://flask-jwt-extended.readthedocs.io/en/stable/
JWT basic usage - https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
"""


def init_jwt_manager(app):
    app.config['JWT_SECRET_KEY'] = get_secret_key()
    JWTManager(app)
