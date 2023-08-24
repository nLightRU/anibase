from flask import Blueprint

users = Blueprint('users', __name__, url_prefix='/')

@users.route('/user/<int:id>')
def user(id):
    return f"<p>user {id}</p>"