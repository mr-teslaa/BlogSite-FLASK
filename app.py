import os
import secrets

#importing necessary module
from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request

# importing form
from forms import RegistrationForm
from forms import LoginForm
from forms import ProfileUpdateForm

# importing db related package
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# importing login hashing
from flask_bcrypt import Bcrypt

#   import module from login manager
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required
from flask_login import LoginManager
from flask_login import UserMixin

# for image editing or saving
from PIL import Image

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


#passing flask engine through 'app' variable
app = Flask(__name__)

#   generate a secret key for forms
app.config['SECRET_KEY'] = 'what  a lovely nigt it is'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_blog.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#   define which route is mendatory if we try to access any unauthorize page.
#   in this case we are trying to access account page but before we access that page we must have to login first.
login_manager.login_view = 'login' # 'login' is the route name

#   beautify the flash message in login page which is authenticate by flask_login
login_manager.login_message_category = 'info' # 'info' is the bootstrap class name what will beautify our alert box

# START ------ db models

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"
# END ------ db models



#default route
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title="About Us")

@app.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('login'))


    return render_template('register.html', title="Registration Page", form=form)

@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Username or Password is incorrect!', 'danger')     
    return render_template('login.html', form=form, title='Login')


#   take picture from local machine and save that into db as hex value
def save_picture(form_picture):
    random_hex = secrets.token_hex(20)
    #   grab the file extention
    # profile.jpg [profile, jpg] [oiwue897348, jpg]
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    #   resize the image using pillow
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#   account route
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile information has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

#   logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug=True
    app.run()


