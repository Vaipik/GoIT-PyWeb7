from flask import current_app as app
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from . import db
from .forms import LoginForm, RegistrationForm, PhoneForm
from .forms import NewRecordBookForm, NewRecordForm, EditRecordBookForm, EditRecordForm
from .models import User, RecordBook, NoteBook
from . import crud


@app.route("/edit_record_book/<string:title>", methods=["GET", "POST"])
@login_required
def edit_record_book(title):

    book = crud.read_record_book(title=title, user=current_user)
    form = EditRecordBookForm(obj=book)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(book)
        book_title = form.title.data
        crud.update_record_book(title=book_title, book=book)
        flash("Book name has been changed")
        return redirect(url_for("record_book", title=book_title))

    return render_template(
        template_name_or_list="edit_record_book.html",
        title=form.title.data,
        form=form
    )


@app.route("/<string:title>/edit_record/<string:record_name>", methods=["GET", "POST"])
@login_required
def edit_record(record_name, title):

    record = crud.read_record(title=title, user=current_user, record_name=record_name)
    form = EditRecordForm(obj=record)
    if request.method == "POST" and form.validate_on_submit():
        form.update_self()
        print(vars(form))
        if form.submit.data:
            # form.populate_obj(record)
            crud.update_record(record=record, form=form)
            flash("Data has been changed successfully")

    return render_template(
        template_name_or_list="edit_record.html",
        form=form,
        title=title
    )


@app.route("/deleting_record_book/<string:title>")
@login_required
def delete_record_book(title):
    book = crud.read_record_book(title=title, user=current_user)
    crud.delete_record_book(book)
    return redirect(url_for("profile", username=current_user.username))


@app.route("/<string:title>/deleting_record/<string:record_name>")
@login_required
def delete_record(title, record_name):
    record = crud.read_record(title=title, user=current_user, record_name=record_name)
    crud.delete_record(record)
    return redirect(url_for("record_book", title=title))


app.route("/")
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


@app.route("/profile/record_book/<string:title>")
@login_required
def record_book(title):
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
        record=record,
        title=title
    )


@app.route("/profile/<string:username>/notebook/<string:book>")
@login_required
def note_book(username, book):
    print(book)
