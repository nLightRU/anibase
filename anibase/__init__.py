import os
from flask import Flask
from flask_migrate import Migrate
from .model import db


def create_app(db_name='anime_db.sqlite'):

    app = Flask(__name__)

    from .anime import anime
    from .users import users

    @app.route('/')
    def home():
        return '<h1>Homepage</h1>'

    app.register_blueprint(anime)
    app.register_blueprint(users)

    # Database setup

    # Legacy from sqlite
    # base_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
    # db_path = os.path.join(base_dir, 'data', db_name)

    db_url = '127.0.0.1:5432'
    db_name = 'anibase_db'
    db_user = 'anibase_app'
    db_pass = 'qwerty12345'
    db_uri = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_url}/{db_name}'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    migrate = Migrate(app, db)
    return app
