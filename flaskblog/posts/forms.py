#   importing  necessary module
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField

#   importing WTF form validation
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField(
            'Title',
            validators = [ DataRequired() ]
    )

    content = TextAreaField(
            'Content',
            validators = [ DataRequired() ]
    )

    submit = SubmitField('Post')