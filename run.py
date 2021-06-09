from song_server.app import create_app
from song_server.shared.configs import *


"""
Entry point, 
Runs the flask app
"""


if __name__ == "__main__":
    app = create_app()
    app.run()
