#   importing basic module
import os
import secrets
from PIL import Image # module for resizing large image
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort

from flaskblog import app
from flaskblog import db
from flaskblog import bcrypt

#   import form class
from flaskblog.forms import RegistrationForm
from flaskblog.forms import LoginForm
from flaskblog.forms import ProfileUpdateForm
from flaskblog.forms import PostForm

#   import db class
from flaskblog.models import User
from flaskblog.models import Post

#   import module from login manager
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required



#   default route
@app.route('/')
@app.route('/home')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

#   about route
@app.route('/about')
def about():
    return render_template('about.html', title="About Us")

#   registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, You can now login', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Registration')

#   login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Username or Password is incorrect!', 'danger')
    return render_template('login.html', form=form, title='Login')

#   login route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#   take picture from local machine and save that into db as hex value
def save_picture(form_picture):
    random_hex = secrets.token_hex(20)
    #   grab the file extention
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    #   resize the image using pillow
    output_size = (125, 125)
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


#   create new post
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form)


#   create single post view route
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


#   create post edit route
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


#   create delete post route
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))