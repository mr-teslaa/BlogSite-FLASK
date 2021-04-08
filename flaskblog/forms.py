from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms import BooleanField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

from flask_login import current_user

from flaskblog.models import User


# registration form
class RegistrationForm(FlaskForm):

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

    submit = SubmitField( 'Sign Up' )

    #   check that username have aleady exits or not
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose another one')

    #   check that email have aleady exits or not
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is taken. Please choose another one')


#   login form
class LoginForm(FlaskForm):

    email = StringField(
        'Email Address',
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

    remember = BooleanField( 'Remember Me' )

    login = SubmitField( 'Login' )


# profie pic update form
class ProfileUpdateForm(FlaskForm):

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

    picture = FileField(
        'Update Profile Picture',
        validators = [
            FileAllowed(
                [
                    'jpg',
                    'png'
                ]
            )
        ]
    )

    submit = SubmitField( 'Update' )

    #   check that username have aleady exits or not
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose another one')

    #   check that email have aleady exits or not
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This email is taken. Please choose another one')



#   create new post form
class PostForm(FlaskForm):

    title = StringField(
        'Title',
        validators = [
            DataRequired()
        ]
    )

    content = TextAreaField(
        'Content',
        validators = [
            DataRequired()
        ]
    )

    submit = SubmitField( 'Post' )