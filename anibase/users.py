from flask import Blueprint, render_template
from flask_login import login_required

users = Blueprint('users', __name__, url_prefix='/')

# We need to check if user is logged in and we need to check if there is a user profile


@users.route('/user/<int:id_user>')
def user(id_user):
    return f"<p>user {id_user}</p>"


@users.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
