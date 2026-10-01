import os
import secrets
from flask import current_app

# for image editing or saving
from PIL import Image


#   take picture from local machine and save that into db as hex value
def save_picture(form_picture):
    random_hex = secrets.token_hex(20)
    #   grab the file extention
    # profile.jpg [profile, jpg] [oiwue897348, jpg]
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    #   resize the image using pillow
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn