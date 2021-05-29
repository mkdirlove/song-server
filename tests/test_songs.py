import pytest

from shared.errorcodes import *
from shared.utils import remove_none_keys
from tests.test_users import test_user_login


@pytest.mark.parametrize(
    "is_explicit, page_number, expected_code, return_code",
    [
        (None, None, 200, SUCCESS),
        # (True, None),
        # (None, 0),
    ]
)
def test_get_all_songs(app, songs_data, is_explicit, page_number,
                       expected_code, return_code):

    body = {'is_explicit': is_explicit, 'page_number': page_number}
    body = remove_none_keys(body)
    request = app.get('/get_songs', json=body)

    # Default transformations
    is_explicit = is_explicit or False
    page_number = page_number or 1

    assert request is not None
    assert request.get_json() is not None

    request_return_code = request.get_json().get('code') or 0
    assert request_return_code == return_code
    assert request.status_code == expected_code

    if request.status_code == 200:
        expected_data = [s.to_json() for s in songs_data
                         if s.is_explicit or not is_explicit]
        expected_data.sort(key=lambda x: x['name'])
        assert request.get_json() == dict(data=expected_data)
