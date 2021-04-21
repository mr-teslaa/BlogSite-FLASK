#   importing necessary module of flask
from flask import render_template
from flask import request
from flask import Blueprint

#   importing post table from database uri
from flaskblog.models import Post

#   creating blueprint
main = Blueprint('main', __name__)


#   default route
@main.route("/")
@main.route("/home")
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)


#   about route
@main.route("/about")
def about():
    return render_template('about.html', title='About')