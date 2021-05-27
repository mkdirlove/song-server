from flask import Flask


def create_app(is_testing=False):
    flask_app = Flask(__name__)
    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run()