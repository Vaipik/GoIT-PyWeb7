import pathlib
import yaml
from os import environ


BASE_DIR = pathlib.Path(__file__).parent.parent

config_file = BASE_DIR / "config" / "config.yaml"


def get_config(path):
    with open(path) as fd:
        config = yaml.safe_load(fd)
        if environ.get("DATABASE_URL", None):
            config["postgres"].update({"url": environ.get("DATABASE_URL")})
    return config


app_config = get_config(config_file)
