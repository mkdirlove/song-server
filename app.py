from flask import Flask
from flask import jsonify

from shared.configs import IS_DEBUG_MODE
from extensions.extinit import init_extensions


def create_app(is_testing=False):
    # Init app
    flask_app = Flask(__name__)
    # Init jwt, mongodb and other external plugins
    init_extensions(flask_app, is_testing)

    # Blueprints importing should be done
    # after db init is complete
    from services.users.routes import bp_user
    from services.songs.routes import bp_songs

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
        return jsonify({'code': e.code, 'message': str(e)}), e.code

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=IS_DEBUG_MODE)