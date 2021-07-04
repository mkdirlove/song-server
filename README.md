
## song-server
A simple flask song server, showing how I'd organize a flask project.

#### Project Structure
```
.
├── song_server                 The song-server application
│   ├── shared                  Modules shared throughout the application
│   │   ├── configs.py          Application configuraitons
│   │   ├── decorators.py       Utility decorators
│   │   ├── utils.py            Utility functions
│   │   └── errorcodes.py       Error codes returned by application
│   ├── extensions              Extensions / Plugins handler & initializer
│   │   ├── dbhelper.py         Mongo db hanlder
│   │   ├── jwthelper.py        Jwt token initializer
│   │   └── extinit.py          Handle extension specific initializations
│   ├── models                  Object models
│   │   ├── song.py             Song model
│   │   └── user.py             User model
│   ├── services                Flask Blueprints
│   │   ├── songs               Blueprints for songs service
│   │   └── users               Blueprints for users service
│   └── app.py                  Flask app creation & initialization
├── tests                       Unit Tests, Load tests and Db population scripts
│   ├── data                    Predefined data, used for tests
│   ├── tests_songs.py          pytest songs service
│   ├── tests_users.py          pytest users service
│   ├── dbpopulate.py           Script to populate db for tests
│   ├── locustfile.py           Locust swarm test
│   └── conftest.py             pytest init and fixtures definition
└── run.py                      Callable entry point to run the server
```

#### Usage
- Clone project
    ```
    git clone https://github.com/agiletelescope/song-server
    cd song-server
    ```
- Create a virtual env
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
- Install requirements
    ```
    pip3 install -r requirements.txt
    ```
- Run server (Ensure **mongod** is running)
    ```
    python3 run.py
    ```
- To run tests
    ```
    pytest -vvs
    ```
- Locust load test
    ```
    locust -f tests/locustfile.py
    ```
- Edit application configs
    ```
    vim ./song_server/shared/configs.py
    ```

#### Return Error Codes

```
SUCCESS = 0
```
```
# Request errors
INVALID_DATA_FORMAT = -1001
DB_OPERATION_FAILURE = -1002
REQUEST_PARSE_ERROR = -1003
INVALID_PAGE_NUMBER = -1004
```

```
# User errors
SIGN_IN_FAILURE = -2001
USERNAME_EXISTS = -2002
USER_PARSE_ERROR = -2003
PRIVILEGE_ERROR = -2004
INVALID_USER_DETAILS = -2005
```

```
# Song errors
SONG_EXISTS = -3001
INVALID_SONG_DETAILS = -3002
SONG_NOT_FOUND = -3003
```
