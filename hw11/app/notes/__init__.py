from flask import Blueprint


bp = Blueprint("notes", __name__, template_folder="templates")


from app.notes import routes
