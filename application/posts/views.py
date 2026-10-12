#   importing necessary module
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort
from flask import Blueprint

#   importing module from flask login
from flask_login import current_user
from flask_login import login_required

#   importing dataase uri
from application import db
from application.models import Post

#   importing WTF froms
from application.posts.forms import PostForm

#   creating the blueprint
posts = Blueprint('posts', __name__)


#   route for creating new post
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('posts/create_post.html', title='New Post', form=form, legend='New Post')