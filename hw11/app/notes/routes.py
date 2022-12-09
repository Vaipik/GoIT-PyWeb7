from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required

from . import bp
from . import crud
from .forms import NewNoteBookForm, NewNoteForm, EditNoteBookForm, EditNoteForm


@bp.route("/edit_note_book/<string:title>", methods=["GET", "POST"])
@login_required
def edit_note_book(title):

    book = crud.read_note_book(title=title, user=current_user)
    form = EditNoteBookForm(obj=book)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(book)
        book_title = form.title.data
        crud.update_note_book(title=book_title, book=book)
        flash("Book name has been changed")
        return redirect(url_for("notes.note_book", title=book_title))

    return render_template(
        template_name_or_list="notes/edit_note  _book.html",
        title=form.title.data,
        form=form
    )


@bp.route("/<string:title>/edit_note/<string:note_title>", methods=["GET", "POST"])
@login_required
def edit_note(note_title, title):
    note = crud.read_note(title=title, user=current_user, note_title=note_title)
    form = EditNoteForm(obj=note)
    if request.method == "POST" and form.validate_on_submit():
        form.update_self()

        if form.submit.data:
            crud.update_note(note=note, form=form)
            flash("Data has been changed successfully")
            return redirect(url_for("notes.show_note", title=title, note_title=form.note_title.data))

    return render_template(
        template_name_or_list="notes/edit_note.html",
        form=form,
        title=title
    )


@bp.route("/deleting_note_book/<string:title>")
@login_required
def delete_note_book(title):
    book = crud.read_note_book(title=title, user=current_user)
    crud.delete_note_book(book)
    return redirect(url_for("profile", username=current_user.username))


@bp.route("/<string:title>/deleting_note/<string:note_title>")
@login_required
def delete_note(title, note_title):
    note = crud.read_note(title=title, user=current_user, note_title=note_title)
    crud.delete_note(note)
    return redirect(url_for("notes.note_book", title=title))


@bp.route("/<string:title>/new_note", methods=["GET", "POST"])
def new_note(title):
    book = crud.read_note_book(title=title, user=current_user)

    form = NewNoteForm()

    if form.validate_on_submit():
        form.update_self()

        if form.submit.data:
            crud.create_note(form=form, title=title)
            return redirect(
                url_for(
                    endpoint="notes.note_book",
                    title=title
                )
            )

    return render_template(
        template_name_or_list="notes/new_note.html",
        book=book,
        form=form
    )


@bp.route("/new_note_book", methods=["GET", "POST"])
@login_required
def new_note_book():
    form = NewNoteBookForm()
    if form.validate_on_submit():
        crud.create_note_book(form=form, user=current_user)
        flash(f"{form.title.data} has been created")
        return redirect(
            url_for(
                endpoint="notes.note_book",
                title=form.title.data
            )
        )

    return render_template(
        template_name_or_list="notes/new_note_book.html",
        title="New note book",
        form=form
    )


@bp.route("/profile/notes/<string:title>")
@login_required
def note_book(title):
    book = crud.read_note_book(title, current_user)
    return render_template(
        template_name_or_list="notes/note_book.html",
        book=book,
    )


@bp.route("/profile/notes/<string:title>/<string:note_title>", methods=["GET"])
@login_required
def show_note(title, note_title):
    note = crud.read_note(title=title, user=current_user, note_title=note_title)
    return render_template(
        template_name_or_list="notes/note.html",
        note=note,
        title=title
    )
