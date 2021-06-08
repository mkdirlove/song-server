
## song-server
A simple flask song server, depicting how I'd organize a flask project

#### Project Structure
```
.
├── song_server                 The song-server application
│   ├── extensions              Extensions / Plugins handler & initializer
│   │   ├── dbhelper.py         Mongo db hanlder
│   │   ├── jwthelper.py        Jwt token initializer
│   │   └── extinit.py          Handle extension specific initializations
│   ├── models                  Object models
│   │   ├── song.py             Song model
│   │   └── user.py             User model
│   ├── services                Flask Blueprints
│   │   ├── songs               Songs blueprints
│   │   └── users               Users blueprints
│   └── app.py                  Flask app creation & initialization
├── tests                       Unit Tests, Load tests and Db population scripts
│   ├── data                    Predefined data, used for tests
│   ├── tests_songs.py          pytest songs service
│   ├── tests_users.py          pytest users service
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
- Edit application configs
    ```
    vim ./song_server/shared/configs.py
    ```

##### Todo

- Db Populate scripts
- Locust load tests
- Stats implementation with song rankings etc.
- Background service for complicated tasks
