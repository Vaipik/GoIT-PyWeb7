from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user

from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from app.auth import bp
from app.auth import crud


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile", username=current_user.username))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("index"))

        login_user(user=user, remember=form.remember_me.data)
        return redirect(url_for("auth.login"))

    return render_template(
        template_name_or_list="auth/login.html",
        title="Sign in",
        form=form
    )


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@bp.route("/registration", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        crud.create_user(form)
        flash("Successful")
        return redirect(url_for("auth.login"))

    return render_template(
        template_name_or_list="auth/register.html",
        title="Registration",
        form=form
    )
