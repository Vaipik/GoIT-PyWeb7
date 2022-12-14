import pathlib

import yaml


BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config" / "app_cfg.yaml"


def get_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


config = get_config(config_path)
