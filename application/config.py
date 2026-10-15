import os

class Config:
    SECRET_KEY = "what  a lovely nigt it is" #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///flask_blog.db" #os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # SMTP setup
    MAIL_SERVER = 'smtp-relay.brevo.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "84288c001@smtp-brevo.com" # os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = "xsmtpsib-xxxxxxxxxx" # os.environ.get('EMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = "ajxxxxxxxxxxxxx@gmail.com"