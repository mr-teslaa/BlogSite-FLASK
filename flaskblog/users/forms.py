#   importing module from WTF
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

#   importing module from flask login. for making sure that the user is logged in
from flask_login import current_user

#   importing user table from database uri
from flaskblog.models import User


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
            validators=[
                DataRequired(),
                Email()
            ]
    )

    password = PasswordField(
            'Password',
            validators = [ DataRequired() ]
    )

    confirm_password = PasswordField(
            'Confirm Password',
            validators = [
                DataRequired(),
                EqualTo('password')
            ]
    )

    submit = SubmitField('Sign Up')

    #   making sure that the username is already exist or not
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    #   making sure that the email is already exist or not
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(
            'Email',
            validators = [
                DataRequired(),
                Email()
            ]
    )

    password = PasswordField(
            'Password',
            validators = [ DataRequired() ]
    )

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
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
                FileAllowed(['jpg', 'png'])
            ]
    )

    submit = SubmitField('Update')

    #   making sure that the username is already exist or not
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    #   making sure that the email is already exist or not
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField(
            'Email',
            validators = [
                DataRequired(),
                Email()
            ]
    )

    submit = SubmitField('Request Password Reset')

    #   making sure that the email is exist in our db or not
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
            'Password',
            validators=[ DataRequired() ]
    )

    confirm_password = PasswordField(
            'Confirm Password',
            validators = [
                DataRequired(),
                EqualTo('password')
            ]
    )

    submit = SubmitField('Reset Password')