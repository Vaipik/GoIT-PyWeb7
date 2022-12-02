import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get("SECRET_KEY") or "123"
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///" + os.path.join(basedir, 'app.db')
	SQLALCHEMY_DATABASE_URI = "mysql://root:password@127.0.0.1:3306/helper"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
