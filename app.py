"""Flask app for Notes."""


import os

from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import RegisterForm, LoginForm, LogoutForm

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

        session["username"] = new_user.username

        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def show_login_form():
    """Display login form or submit login form."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        user = User.authenticate(name, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Bad name/password']

    else:
        flash('how did you get here?')

    return render_template("login.html", form=form)


@app.post('/logout')
def logout_user():
    """Logs out user from session and redirects to root route."""

    form = LogoutForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')


@app.get('/users/<username>')
def show_user_details(username):
    """Show template of user (everything except password)"""

    form = LogoutForm()
    # check if passed in username = session username

    if session.get("username") == username:

        user = User.query.filter_by(username=username).one_or_none()

        return render_template("user_detail.html", user=user, form=form)
    else:
        flash('Please log in as that user to view that page')
        return redirect('/')
