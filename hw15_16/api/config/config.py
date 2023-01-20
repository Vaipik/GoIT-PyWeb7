import pathlib

from dotenv import dotenv_values

BASE_DIR = pathlib.Path(__file__).parent

app_config = dotenv_values(BASE_DIR / ".env")
