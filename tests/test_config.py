from copydata.config import build_from_json


def test_build_from_json():
    json = r'{"test": "test"}'
    config = build_from_json(json)
    assert config.validate() is False
