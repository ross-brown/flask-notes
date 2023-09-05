"""Flask app for Notes."""


import os

from flask import Flask, jsonify, request, render_template, redirect, session, flash, abort
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, CSRFForm, NoteForm, EditNoteForm

AUTH_KEY = "username"

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.get("/")
def show_homepage():
    """Redirect to register page."""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def show_register_form():
    """Display register form or submit register form."""

    if session.get(AUTH_KEY):
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session[AUTH_KEY] = new_user.username

        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def show_login_form():
    """Display login form or submit login form."""

    if session.get(AUTH_KEY):
        return redirect(f"/users/{session[AUTH_KEY]}")

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        user = User.authenticate(name, password)

        if user:
            session[AUTH_KEY] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Bad name/password']

    return render_template("login.html", form=form)


@app.post('/logout')
def logout_user():
    """Logs out user from session and redirects to root route."""

    form = CSRFForm()

    if form.validate_on_submit():
        session.pop(AUTH_KEY, None)

    return redirect('/')


@app.get('/users/<username>')
def show_user_details(username):
    """Show template of user (everything except password)"""

    if session.get(AUTH_KEY) == username:
        form = CSRFForm()

        user = User.query.filter_by(username=username).one_or_none()

        return render_template("user_detail.html", user=user, form=form, notes=user.notes)
    else:
        flash('Please log in as that user to view that page')
        return redirect('/')

# TODO: add comments to separate sections of routes
# POST /users/<username>/delete
#     Remove the user from the database. Log the user out and redirect to /.


@app.post("/users/<username>/delete")
def delete_user(username):
    """Delete user from DB and redirect to homepage."""
    if session.get(AUTH_KEY) == username:
        user = User.query.get(username)
        notes = user.notes

        for note in notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        session.pop(AUTH_KEY, None)  # logout user

        return redirect("/")
    else:
        abort(401)


@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def show_add_note_form(username):
    """Display add note form or adds note and redirects to user profile."""
    if not session.get(AUTH_KEY) == username:
        return redirect('/')

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(title=title, content=content, owner_username=username)

        db.session.add(new_note)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        user = User.query.get(username)
        return render_template('add_note.html', user=user, form=form)
# GET /users/<username>/notes/add
#     Display form to add notes.

# POST /users/<username>/notes/add
#     Add a new note and redirect to /users/<username>


@app.route('/notes/<int:note_id>/update', methods=["GET", "POST"])
def show_edit_note_form(note_id):
    """Display form and edit notes"""
    note = Note.query.get(note_id)
    username = note.user.username

    if not session.get(AUTH_KEY) == username:
        return redirect('/')

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note.title = title
        note.content = content

        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template('edit_note.html', form=form)

# GET /notes/<note-id>/update
#     Display form to edit a note.

# POST /notes/<note-id>/update
#     Update a note and redirect to /users/<username>.


@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """Deletes a note and redirects"""

    form = CSRFForm()

    if form.validate_on_submit():
        note = Note.query.get(note_id)
        user = note.user

        if session[AUTH_KEY] == user.username:

            db.session.delete(note)
            db.session.commit()

        return redirect(f"/users/{user.username}")

    else:
        return redirect("/")
# POST /notes/<note-id>/delete
#     Delete a note and redirect to /users/<username>.
