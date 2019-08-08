import pytest

from copydata.config import Config


@pytest.fixture
def sample_config():
    return Config("path")
