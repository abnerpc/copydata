import json

from .exceptions import ConfigError

from . import datasources


class Config:

    origin_datasource = None
    target_datasource = None

    def __init__(self, origin, target):
        if not origin or not target:
            raise ConfigError("Missing required origin or target config.")

        self.origin_datasource.

        pass

    @classmethod
    def build_from_json(cls, json_text):
        config_json = json.loads(json_text)
        return cls(**config_json)

    def validate(self):
        return False

