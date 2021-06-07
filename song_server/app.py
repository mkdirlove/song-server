from flask import Flask
from flask import jsonify

from song_server.shared.configs import DevConfig, TestConfig
from song_server.extensions.extinit import init_extensions


def create_app(is_testing=False):

    # Init app
    flask_app = Flask(__name__)
    flask_app.config.from_object(
        TestConfig if is_testing else DevConfig)

    # Init jwt, mongodb and other external plugins
    init_extensions(flask_app)

    # Blueprints importing should be done
    # after db init is complete
    from song_server.services.users.routes import bp_user
    from song_server.services.songs.routes import bp_songs

    # Register blueprints
    flask_app.register_blueprint(bp_user)
    flask_app.register_blueprint(bp_songs)

    # Generic Error Handlers
    @flask_app.errorhandler(400)  # Bad request
    @flask_app.errorhandler(401)  # Un-authorized
    @flask_app.errorhandler(404)  # Not found
    @flask_app.errorhandler(405)  # method not allowed
    @flask_app.errorhandler(500)  # Internal server error
    def error_handler(e):
        return jsonify({'code': e.description, 'message': str(e)}), e.code

    return flask_app
