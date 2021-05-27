from flask import Flask

from shared.configs import IS_DEBUG_MODE
from extensions.extinit import init_extensions


def create_app(is_testing=False):
    # Init app
    flask_app = Flask(__name__)
    # Init jwt, mongodb and other external plugins
    init_extensions(flask_app, is_testing)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=IS_DEBUG_MODE)