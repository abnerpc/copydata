from unittest import mock

import pytest

from copydata.config import Config, build_config


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


@pytest.mark.parametrize(
    "raw_config,datasource_values,expected_error,expected_calls",
    [
        (
            {"origin": {"type": "regular", "test": "1"}, "targets": []},
            [None],
            "Datasource not found for type regular.",
            [mock.call("regular", {"test": "1"})]
        ),
        (
            {"origin": {"type": "regular", "test": "2"}, "targets": [{"type": "target_1"}]},
            ["first_source", None],
            "Datasource not found for type target_1.",
            [mock.call("regular", {"test": "2"}), mock.call("target_1", {})]
        ),
        (
            {"origin": {"type": "regular", "test": "3"}, "targets": [{"type": "target_1"}, {"type": "target_2"}]},
            ["first_source", "first_target", None],
            "Datasource not found for type target_2.",
            [mock.call("regular", {"test": "3"}), mock.call("target_1", {}), mock.call("target_2", {})]
        ),
        (
            {"origin": {"type": "regular", "test": "4"}, "targets": [{"type": "target_1"}, {"type": "target_2"}]},
            ["first_source", "first_target", "second_target"],
            None,
            [mock.call("regular", {"test": "4"}), mock.call("target_1", {}), mock.call("target_2", {})]
        ),
    ],
    ids=[
        "with wrong origin type",
        "with valid origin and one invalid target",
        "with valid origin, one valid and one invalid",
        "with valid origin and two valid targets",
    ]
)
@mock.patch("copydata.config.get_data_source")
def test_config_build_datasources(
    mocked_get_data_source,
    raw_config,
    datasource_values,
    expected_error,
    expected_calls,
    sample_config
):
    sample_config.raw_config = raw_config
    mocked_get_data_source.side_effect = datasource_values

    error = sample_config.build_datasources()
    assert error == expected_error
    mocked_get_data_source.assert_has_calls(expected_calls)


@mock.patch("copydata.config.Config.build_datasources")
@mock.patch("copydata.config.Config.validate")
def test_build_config_with_config_error(mocked_validate, mocked_build_datasources):
    mocked_validate.return_value = "error at config"
    config, result = build_config("path")
    assert result == "error at config"
    mocked_validate.assert_called_once_with()
    mocked_build_datasources.assert_not_called()


@mock.patch("copydata.config.Config.build_datasources")
@mock.patch("copydata.config.Config.validate")
def test_build_config_with_datasource_error(mocked_validate, mocked_build_datasources):
    mocked_validate.return_value = None
    mocked_build_datasources.return_value = "error at datasource"
    config, result = build_config("path")
    assert result == "error at datasource"
    mocked_validate.assert_called_once_with()
    mocked_build_datasources.assert_called_once_with()
