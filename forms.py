from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional, URL, Email


class RegisterForm(FlaskForm):
    """Form for Registering a user"""

    username = StringField("Username: ", validators=[InputRequired()])

    password = StringField("Password: ", validators=[InputRequired()])

    #FIXME: We want to validate that this is email, need to pip install something.
    email = StringField("Email: ", validators=[InputRequired()])

    first_name = StringField("First Name: ", validators=[InputRequired()])

    last_name = StringField("Last Name: ", validators=[InputRequired()])


    # def validate_email(self):


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])

    password = StringField("Password: ", validators=[InputRequired()])
