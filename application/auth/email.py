#   importing necessary module
import os
import secrets
from PIL import Image
from flask import url_for
from flask import current_app
from flask import request
from flask import render_template
from flask_mail import Message
from application import mail
from application.auth.location import getLocation
from application import db

# ===================================
#     SEND ACCOUNT ACTIVATION EMAIL
# ===================================
def send_activation_email(user):
    ip_request = request.remote_addr
    getlocation = getLocation(ip_request)
    location = getlocation.get("country")
    if location is None:
        location = "Unknown Location"
        
    token = user.generate_activation_token()
    user.activation_token = token
    db.session.commit()
    activation_url = url_for("auth.activate", token=token, _external=True)
    msg = Message(
        "[FLASK BLOG] Activate your account",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
    )
    msg.html = render_template(
        "emails/send_activation_email.html", 
        user=user, 
        location=location, 
        ip=ip_request, 
        activation_link=activation_url
    )
    mail.send(msg)