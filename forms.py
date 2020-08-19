from flask_wtf import FlaskForm
from wtforms import StringField
from wtfroms import PasswordField
from wtfroms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo





Class RegistrationForm(FlaskForm):

    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators = [
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Sign Up')