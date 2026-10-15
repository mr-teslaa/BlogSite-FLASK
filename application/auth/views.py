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
from application.auth.forms import RegistrationForm
from application.auth.forms import LoginForm

# SMTP EMAIL SENDING MODULE
from application.auth.email import send_activation_email

#   creating blueprint
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
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
        
        # SEND ACTIVATION EMAIL TO USER
        send_activation_email(user)

        flash('User registered successfully', 'success')
        return redirect(url_for('auth.login'))


    return render_template('register.html', title="Registration Page", form=form)

@auth.route('/login', methods=['GET', 'POST'])
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
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# ACTIVATE TOKEN VAERIFY
@auth.route('/activate/<token>')
def activate(token):
    # Activate a user's account
    user = User.query.filter_by(activation_token=token).first()

    if user.is_active == True:
        flash('Your account is already active. Please login to continue', 'success')
        return redirect(url_for('auth.login'))
    
    if user:
        user_verified = user.verify_reset_token(token)
        if user_verified:
            user.is_active = True
            db.session.commit()
            flash('Your account has been activated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('The activation link is invalid or has expired.', 'warning')
        return redirect(url_for('auth.join'))
