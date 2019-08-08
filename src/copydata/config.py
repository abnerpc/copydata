import json
from json.decoder import JSONDecodeError


class Config:

    path = None
    origin = None
    targets = None

    def __init__(self, path):
        self.path = path

    def validate(self):
        """
        Validate config file

        Returns:
            str: Error message
        """
        raw_config = None
        try:
            with open(self.path, "r") as config_file:
                raw_config = json.loads(config_file.read())
        except FileNotFoundError:
            return f"Config file not found. {self.path}"
        except JSONDecodeError:
            return f"Invalid config file format. {self.path}"

        has_required_keys = all([c in raw_config for c in ("origin", "targets")])
        if not has_required_keys:
            return f"Missing required origin or targets config."
