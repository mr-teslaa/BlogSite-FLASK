#   importing necessary module
from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect

#   import form class
from forms import RegistrationForm
from forms import LoginForm

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

#   default route
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)

#   registration route
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('registar.html', form=form, title='Registration')

#   login route
@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'{form.username.data}, You have successfully login!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Login')

#   about route
@app.route('/about')
def about():
    return render_template('about.html', title="About Us")



if __name__ == "__main__":
    app.debug=True
    app.run()