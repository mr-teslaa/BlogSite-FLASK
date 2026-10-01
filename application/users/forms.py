from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField

from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo



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