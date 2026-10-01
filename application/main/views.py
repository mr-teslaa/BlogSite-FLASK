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

# importing forms
from application.main.forms import RegistrationForm
from application.main.forms import LoginForm

#   creating blueprint
main = Blueprint('main', __name__)


posts =[
    {
        'author': 'tesla',
        'title': 'first post',
        'content': 'no more google, gmail, tracking. use duckduckgo.com',
        'date_posted': '01 July 2020'
    },
    {
        'author': 'sefuda',
        'title': 'second post',
        'content': 'no more youtube. use protonmail.com',
        'date_posted': '01 July 2020'
    }
]


#default route
@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title="About Us")

@main.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        print('------ form submitted -------')
        print('Username -->', form.username.data)
        print('Email -->', form.email.data)
        print('Password -->', form.password.data)

        # SAVE USER IN DB 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully', 'success')
        return redirect(url_for('main.login'))


    return render_template('register.html', title="Registration Page", form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Login form email: ', form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        # print('Checking db: ', user)
        # print('username from db: ', user.username)
        # print('email from db: ', user.email)
        # print('password from db: ', user.password)
        # print('checking hash is matching with db: ', bcrypt.check_password_hash(user.password, form.password.data))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Username or Password is incorrect!', 'danger')     
    return render_template('login.html', form=form, title='Login')


#   logout route
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))