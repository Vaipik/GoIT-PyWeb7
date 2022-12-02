from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app() -> Flask:
	
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object("config.Config")

	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	login.login_view = "login"

	with app.app_context():
		from . import routes
		db.create_all()

	return app
	
	
