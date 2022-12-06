from flask import current_app as app
from flask import request, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.orm import joinedload

from . import db
from .forms import LoginForm, RegistrationForm, NewRecordBookForm, NewRecordForm
from .models import User, RecordBook, NoteBook
from . import crud


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


@app.route("/<string:title>/new_record", methods=["GET", "POST"])
def new_record(title):

    book = crud.read_record_book(title=title, user=current_user)

    form = NewRecordForm()
    if form.validate_on_submit():
        form.update_self()

        if form.submit.data:
            crud.create_record(form=form, title=title, user=current_user)

            return redirect(
                url_for(
                    endpoint="record_book",
                    title=title
                )
            )

    return render_template(
        template_name_or_list="new_record.html",
        book=book,
        form=form
    )


@app.route("/new_record_book", methods=["GET", "POST"])
@login_required
def new_record_book():

    form = NewRecordBookForm()
    if form.validate_on_submit():
        crud.create_record_book(form=form, user=current_user)
        flash(f"{form.title.data} has been created")
        return redirect(
            url_for(
                endpoint="record_book",
                title=form.title.data
            )
        )

    return render_template(
        template_name_or_list="new_record_book.html",
        title="New record book",
        form=form
    )


@app.route("/profile/record_book/<string:title>")
@login_required
def record_book(title, **kwargs):
    book = crud.read_record_book(title, current_user)

    return render_template(
        template_name_or_list="record_book.html",
        book=book,
    )


@app.route("/profile/<string:title>/<string:record_name>", methods=["GET"])
@login_required
def show_record(title, record_name):
    record = crud.read_record(title=title, user=current_user, record_name=record_name)
    return render_template(
        template_name_or_list="record.html",
        record=record
    )


@app.route("/profile/<string:username>/notebook/<string:book>")
@login_required
def note_book(username, book):
    print(book)

