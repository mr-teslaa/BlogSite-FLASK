# import flask related package
from flask import Flask

# importing db related package
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# importing login hashing
from flask_bcrypt import Bcrypt

#   import module from login manager
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required
from flask_login import LoginManager
from flask_login import UserMixin

from application.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

#   define which route is mendatory if we try to access any unauthorize page.
#   in this case we are trying to access account page but before we access that page we must have to login first.
login_manager.login_view = 'main.login' # 'login' is the route name

#   beautify the flash message in login page which is authenticate by flask_login
login_manager.login_message_category = 'info' # 'info' is the bootstrap class name what will beautify our alert box


def create_app(config_class=Config):
    #passing flask engine through 'app' variable
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from application.users.views import users
    app.register_blueprint(users)

    from application.main.views import main
    app.register_blueprint(main)
    # from flaskblog.posts.routes import posts
    # from flaskblog.errors.handlers import errors
    # app.register_blueprint(posts)
    # app.register_blueprint(errors)

    return app