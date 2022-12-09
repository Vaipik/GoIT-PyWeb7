from flask import Blueprint


bp = Blueprint("records", __name__, template_folder="templates")


from . import routes
