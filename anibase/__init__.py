from flask import Flask
from .model import db_uri


def create_app():

    app = Flask(__name__)

    from .anime import anime
    from .users import users

    @app.route('/')
    def home():
        return '<h1>Homepage</h1>'

    app.register_blueprint(anime)
    app.register_blueprint(users)

    # Database setup
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    return app
