import os

from dotenv import load_dotenv
from flask import Flask

from flask_wtf.csrf import CSRFProtect

from .dbmanager import DBManager
from .auth import login_manager

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')

url = f'postgresql://{user}:{password}@{host}/{database}'

db = DBManager(url)


def create_app():
    app = Flask(__name__)

    # Random secret key for development purposes
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['PER_PAGE'] = 20

    from .views import views
    from .anime import anime
    from .auth import auth
    from .users import users

    app.register_blueprint(anime)
    app.register_blueprint(views)
    app.register_blueprint(users)
    app.register_blueprint(auth)

    # Users: CSRF protection and users management
    csrf = CSRFProtect()
    csrf.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    return app
