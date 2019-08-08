import pytest

from copydata.datasources import get_data_source, HttpDataSource, DatabaseDataSource


@pytest.mark.parametrize("_type,expected", [
    ("x", type(None)),
    ("http", HttpDataSource),
    ("database", DatabaseDataSource),
])
def test_get_data_source(_type, expected):
    result = get_data_source(_type, {})
    assert isinstance(result, expected)
