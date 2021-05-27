from flask import Flask

from shared.configs import *


def create_app(is_testing=False):
    flask_app = Flask(__name__)
    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=IS_DEBUG_MODE)