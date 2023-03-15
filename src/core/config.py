import json


class Config:
    # TODO find / create better solution
    config = None

    @staticmethod
    def get_config(path: str) -> dict:
        if Config.config is None:
            config_file = open(path)
            Config.config = json.load(config_file)

        return Config.config
