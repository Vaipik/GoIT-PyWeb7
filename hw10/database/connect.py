import configparser
import pathlib

from mongoengine import connect


config_file = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(config_file)

mongo_user = config.get("DB", "user")
mongo_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
    ssl=True
)
