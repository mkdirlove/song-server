import pytest

from shared.errorcodes import *
from shared.configs import *
from shared.utils import remove_none_keys


@pytest.mark.parametrize(
    "is_filter_explicit, page_number, expected_code, return_code",
    [
        # None data
        (None, None, 200, SUCCESS),
        (True, None, 200, SUCCESS),
        (None, 0, 200, SUCCESS),

        # page-number
        (None, -1, 400, INVALID_DATA_FORMAT),
        (None, -999, 400, INVALID_DATA_FORMAT),
        (None, 1, 200, SUCCESS),
        (None, 99999, 200, SUCCESS),

        # is-filter-explicit
        (True, 1, 200, SUCCESS),
        (False, 1, 200, SUCCESS),
    ]
)
def test_get_all_songs(app, songs_data, is_filter_explicit, page_number,
                       expected_code, return_code):

    body = {
        'is_filter_explicit': is_filter_explicit,
        'page_number': page_number
    }
    body = remove_none_keys(body)
    request = app.get('/get_songs', json=body)

    assert request is not None
    assert request.get_json() is not None

    request_return_code = request.get_json().get('code') or 0
    assert request_return_code == return_code
    assert request.status_code == expected_code

    if request.status_code == 200:

        # default transformations within request
        is_filter_explicit = is_filter_explicit or False
        page_number = page_number or 1

        expected_data = [s.to_json() for s in songs_data
                         if not s.is_explicit or not is_filter_explicit]
        expected_data.sort(key=lambda x: x['name'])
        start_index = (page_number - 1) * DB_ENTRIES_PER_PAGE
        expected_data = expected_data[
                        start_index:start_index+DB_ENTRIES_PER_PAGE]

        assert request.get_json() is not None
        assert 'data' in request.get_json()
        assert request.get_json() == dict(data=expected_data)
