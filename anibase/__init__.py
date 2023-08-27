from os import path
from  flask import Flask
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
    base_dir = path.abspath(path.join(path.abspath(path.dirname(__file__)), '..'))
    db_path = path.join(base_dir, 'data', db_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    db.init_app(app)

    return app
