from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, Email, Length


class RegisterForm(FlaskForm):
    """Form for Registering a user"""

    username = StringField("Username: ", validators=[
                           InputRequired(), Length(max=20)])

    password = PasswordField("Password: ", validators=[
        InputRequired(), Length(max=100)])

    email = StringField("Email: ", validators=[
                        InputRequired(), Email(), Length(max=50)])

    first_name = StringField("First Name: ", validators=[
                             InputRequired(), Length(max=30)])

    last_name = StringField("Last Name: ", validators=[
                            InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username: ", validators=[
                           InputRequired(), Length(max=20)])

    password = PasswordField("Password: ", validators=[
        InputRequired(), Length(max=100)])


class CSRFForm(FlaskForm):
    """ Form just for CSRF Protection"""


class NoteForm(FlaskForm):
    """Form for adding/editing notes."""
    title = StringField("Title: ", validators=[
                        InputRequired(), Length(max=100)])

    content = TextAreaField("Content: ", validators=[
                            InputRequired()])

#TODO: use this
class EditNoteForm(NoteForm):
    """Form for editing notes."""
