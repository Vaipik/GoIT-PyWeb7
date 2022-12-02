from flask import current_app as app
from flask import request, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required

from . import db
from .forms import LoginForm, RegistrationForm
from .models import User, RecordBook, NoteBook


@app.route("/")
@app.route("/index")
@login_required
def index():

    if current_user.is_authenticated:
        return redirect(url_for("profile", username=current_user.username))

    return render_template(
        template_name_or_list="index.html",
    )


@app.route("/login", methods=["GET", "POST"])
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
        return redirect(url_for("login"))

    return render_template(
        template_name_or_list="login.html",
        title="Sign in",
        form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile/<string:username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user:
        record_books = RecordBook.query.filter_by(user=user)
        note_books = NoteBook.query.filter_by(user=user)
        return render_template(
            template_name_or_list="profile.html",
            user=user,
            record_books=record_books,
            note_books=note_books
        )

    return redirect(url_for("login"))


@app.route("/registration", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successful")
        return redirect(url_for("login"))

    return render_template(
        template_name_or_list="register.html",
        title="Registration",
        form=form
    )
