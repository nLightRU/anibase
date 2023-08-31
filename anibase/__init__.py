from flask import Flask
from .model import db_uri


def create_app():

    app = Flask(__name__)

    from .views import views
    from .users import users

    app.register_blueprint(views)
    app.register_blueprint(users)

    # Database setup
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    return app
