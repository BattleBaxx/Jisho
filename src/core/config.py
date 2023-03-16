import json
from pathlib import Path

current_path = Path(__file__)
config_path = current_path.parents[2] / "config.json"


class Config:
    config = None

    @staticmethod
    def get_config() -> dict:
        if Config.config is None:
            config_contents = open(config_path).read(-1)
            Config.config = json.loads(config_contents)

        return Config.config
