import os

class Config:
    SECRET_KEY = "what  a lovely nigt it is" #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///flask_blog.db" #os.environ.get('SQLALCHEMY_DATABASE_URI')