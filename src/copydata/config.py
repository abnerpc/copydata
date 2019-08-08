import json
from json.decoder import JSONDecodeError

from .datasources import get_data_source


class Config:

    path = None
    raw_config = None
    origin = None
    targets = []

    def __init__(self, path):
        self.path = path

    def validate(self):
        """
        Validate config file

        Returns:
            str: Error message
        """
        try:
            with open(self.path, "r") as config_file:
                self.raw_config = json.loads(config_file.read())
        except FileNotFoundError:
            return f"Config file not found. {self.path}"
        except JSONDecodeError:
            return f"Invalid config file format. {self.path}"

        has_required_keys = all([c in self.raw_config for c in ("origin", "targets")])
        if not has_required_keys:
            return f"Missing required origin or targets config."

    def build_datasources(self):
        origin_config = self.raw_config["origin"]
        _type = origin_config.pop("type", None)
        self.origin = get_data_source(_type, origin_config)
        if not self.origin:
            return f"Datasource not found for type {_type}."

        targets = self.raw_config["targets"]
        for target_config in targets:
            _type = target_config.pop("type", None)
            target = get_data_source(_type, target_config)
            if not target:
                return f"Datasource not found for type {_type}."
            self.targets.append(target)


def build_config(path):
    config = Config(path)
    error = config.validate()
    if not error:
        error = config.build_datasources()

    return config, error
