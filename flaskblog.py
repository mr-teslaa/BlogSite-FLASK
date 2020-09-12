#   importing necessary module
from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect

#   importing database uri
from flask_sqlalchemy import SQLAlchemy

#   import form class
from forms import RegistrationForm
from forms import LoginForm

#   creating class for database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=Flase)
    email = db.Column(db.String(120), unique=True, nullable=Flase)
    image_file = db.Column(db.String(20), nullable=Flase, deflault='default.jpg')
    password = db.Column(db.String(60), nullable=Flase)

    def __repr__(slef):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class post

    #   next day. code will be goes here


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
        'date_posted': '28 July 2020'
    }
]


#   passing flask engine through 'app' variable
app = Flask(__name__)

#   generate a secret key for forms
app.config['SECRET_KEY'] = '94692de71c05d2759ecc4bfd5d5ec4f0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#   default route
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)

#   registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Registration')

#   login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@protonmail.com' and form.password.data == 'admin':
            flash(f'You have successfully logegd in!', 'success') 
            return redirect( url_for('index') )
        else:
            flash(f'Username or Password is incorrect!', 'danger')      
    return render_template('login.html', form=form, title='Login')

#   about route
@app.route('/about')
def about():
    return render_template('about.html', title="About Us")



if __name__ == "__main__":
    app.debug=True
    app.run()