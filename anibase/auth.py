import flask
from flask import Blueprint, render_template, request
from flask import redirect

from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .model import engine, User
from .forms import RegistrationForm, LoginForm

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, password_hash=form.password.data)
            # flask.flash(f"{form.username.data}, {form.password.data}")
            try:
                with Session(engine) as session:
                    session.add(user)
                    session.commit()
            except SQLAlchemyError:
                return render_template('signup.html', reg_form=form)
        return render_template('index.html')

    return render_template('signup.html', reg_form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect('/profile', code=302, Response=None)

    return render_template('login.html', login_form=form)



