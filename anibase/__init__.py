from flask import Flask


def create_app():

    app = Flask(__name__)

    from .anime import anime
    from .users import users

    @app.route('/')
    def home():
        return '<h1>Homepage</h1>'

    app.register_blueprint(anime)
    app.register_blueprint(users)

    return app
