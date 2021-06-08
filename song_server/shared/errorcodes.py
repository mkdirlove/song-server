# List of all error codes the api returns

SUCCESS = 0

# Request errors
INVALID_DATA_FORMAT = -1001
DB_OPERATION_FAILURE = -1002
REQUEST_PARSE_ERROR = -1003
INVALID_PAGE_NUMBER = -1004

# User errors
SIGN_IN_FAILURE = -2001
USERNAME_EXISTS = -2002
USER_PARSE_ERROR = -2003
PRIVILEGE_ERROR = -2004
INVALID_USER_DETAILS = -2005

# Song errors
SONG_EXISTS = -3001
INVALID_SONG_DETAILS = -3002
SONG_NOT_FOUND = -3003
