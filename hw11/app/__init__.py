from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
csrf = CSRFProtect()

"""TO AVOID CYCLIC IMPORT"""
from app.auth import bp as auth_bp
from app.notes import bp as note_bp
from app.records import bp as rec_bp
"""AVOIDED"""

def create_app() -> Flask:

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    app.register_blueprint(auth_bp)
    app.register_blueprint(rec_bp)
    app.register_blueprint(note_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    login.login_view = "login"

    with app.app_context():
        from app import routes
        db.create_all()

    return app
