from unittest import mock

import pytest

from copydata.config import Config


def test_config_validate_invalid_path():
    config = Config("invalid_path")
    error = config.validate()
    assert error == "Config file not found. invalid_path"


def test_config_validate_invalid_json():
    mocked_open = mock.mock_open(read_data='invalid_json')
    with mock.patch('copydata.config.open', mocked_open):
        config = Config("path")
        error = config.validate()
        assert error == "Invalid config file format. path"


@pytest.mark.parametrize("config", [
    '{"test": "hey"}',
    '{"origin": "testing"}',
    '{"targets": "another test"}'
])
def test_config_validate_without_required_keys(config):
    mocked_open = mock.mock_open(read_data=config)
    with mock.patch('copydata.config.open', mocked_open):
        config = Config("path")
        error = config.validate()
        assert error == "Missing required origin or targets config."


def test_config_validate_valid():
    mocked_open = mock.mock_open(read_data='{"origin": "1", "targets": "2"}')
    with mock.patch('copydata.config.open', mocked_open):
        config = Config("path")
        assert config.validate() is None
    mocked_open.assert_called_once_with("path", "r")
