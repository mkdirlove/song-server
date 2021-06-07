from song_server.shared.configs import *
from song_server.app import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=IS_DEBUG_MODE)
