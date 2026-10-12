# importing flask modules
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import request
from flask import url_for

# importing package
from application import bcrypt
from application import db
from flask_login import login_user
from flask_login import logout_user

# importing models
from application.models import User
from application.models import Post

# importing forms
from application.auth.forms import RegistrationForm
from application.auth.forms import LoginForm

#   creating blueprint
main = Blueprint('main', __name__)


# posts =[
#     {
#         'author': 'tesla',
#         'title': 'first post',
#         'content': 'no more google, gmail, tracking. use duckduckgo.com',
#         'date_posted': '01 July 2020'
#     },
#     {
#         'author': 'sefuda',
#         'title': 'second post',
#         'content': 'no more youtube. use protonmail.com',
#         'date_posted': '01 July 2020'
#     }
# ]


#default route
@main.route('/')
@main.route('/home')
def index():
    posts = Post.query.all()
    print('---- posts ----')
    print(posts)
    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title="About Us")

