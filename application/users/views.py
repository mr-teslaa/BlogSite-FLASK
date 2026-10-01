# flask necessary module import
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import render_template

# flask login package import
from flask_login import login_required
from flask_login import current_user

# database improt
from application import db

# forms
from application.users.forms import ProfileUpdateForm

# utils
from application.utils import save_picture

users = Blueprint('users', __name__)

#   account route
@users.route('/account', methods=['GET', 'POST'])
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

