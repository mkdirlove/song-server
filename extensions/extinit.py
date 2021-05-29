from shared.utils import populate_admin_user
from extensions.jwthelper import init_jwt_manager
from extensions.dbhelper import init_db


def init_extensions(app, is_testing):

    if app is None:
        raise ValueError('Flask app can\'t be None')

    # Init Json web tokens
    init_jwt_manager(app)

    # Init db
    init_db(is_testing)

    # Init the first admin user
    populate_admin_user()
