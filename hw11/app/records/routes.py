from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required

from app.records import bp
from . import crud
from .forms import NewRecordBookForm, NewRecordForm, EditRecordBookForm, EditRecordForm


@bp.route("/edit_record_book/<string:title>", methods=["GET", "POST"])
@login_required
def edit_record_book(title):

    book = crud.read_record_book(title=title, user=current_user)
    form = EditRecordBookForm(obj=book)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(book)
        book_title = form.title.data
        crud.update_record_book(title=book_title, book=book)
        flash("Book name has been changed")
        return redirect(url_for("records.record_book", title=book_title))

    return render_template(
        template_name_or_list="records/edit_record_book.html",
        title=form.title.data,
        form=form
    )


@bp.route("/<string:title>/edit_record/<string:record_name>", methods=["GET", "POST"])
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
        template_name_or_list="records/edit_record.html",
        form=form,
        title=title
    )


@bp.route("/deleting_record_book/<string:title>")
@login_required
def delete_record_book(title):
    book = crud.read_record_book(title=title, user=current_user)
    crud.delete_record_book(book)
    return redirect(url_for("profile", username=current_user.username))


@bp.route("/<string:title>/deleting_record/<string:record_name>")
@login_required
def delete_record(title, record_name):
    record = crud.read_record(title=title, user=current_user, record_name=record_name)
    crud.delete_record(record)
    return redirect(url_for("records.record_book", title=title))


@bp.route("/<string:title>/new_record", methods=["GET", "POST"])
def new_record(title):
    book = crud.read_record_book(title=title, user=current_user)

    form = NewRecordForm()

    if form.validate_on_submit():
        form.update_self()
        if form.submit.data:
            crud.create_record(form=form, title=title, user=current_user)
            return redirect(
                url_for(
                    endpoint="records.record_book",
                    title=title
                )
            )

    return render_template(
        template_name_or_list="records/new_record.html",
        book=book,
        form=form
    )


@bp.route("/new_record_book", methods=["GET", "POST"])
@login_required
def new_record_book():
    form = NewRecordBookForm()
    if form.validate_on_submit():
        crud.create_record_book(form=form, user=current_user)
        flash(f"{form.title.data} has been created")
        return redirect(
            url_for(
                endpoint="records/record_book",
                title=form.title.data
            )
        )

    return render_template(
        template_name_or_list="new_record_book.html",
        title="New record book",
        form=form
    )


@bp.route("/profile/records/<string:title>")
@login_required
def record_book(title):
    book = crud.read_record_book(title, current_user)

    return render_template(
        template_name_or_list="records/record_book.html",
        book=book,
    )


@bp.route("/profile/<string:title>/<string:record_name>", methods=["GET"])
@login_required
def show_record(title, record_name):
    record = crud.read_record(title=title, user=current_user, record_name=record_name)
    return render_template(
        template_name_or_list="records/record.html",
        record=record,
        title=title
    )
