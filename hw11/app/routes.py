from flask import current_app as app
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app.auth import crud as auth_crud


@app.route("/")
@app.route("/index")
@login_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for("profile", username=current_user.username))

    return render_template(
        template_name_or_list="index.html",
    )


@app.route("/profile/<string:username>")
@login_required
def profile(username):
    user = auth_crud.read_user(username)
    if user:
        return render_template(
            template_name_or_list="profile.html",
            user=user
        )

    return redirect(url_for("auth.login"))
