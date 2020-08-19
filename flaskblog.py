#importing necessary module
from flask import Flask
from flask import render_template
from flask import url_for


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

#default route
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title="About Us")



if __name__ == "__main__":
    app.debug=True
    app.run()