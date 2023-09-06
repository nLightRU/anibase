from flask import Blueprint, render_template, request
from flask import redirect
from flask_wtf import CSRFProtect

from werkzeug.security import generate_password_hash

from sqlalchemy import exc
from sqlalchemy.orm import Session

from .model import engine, User
from .forms import RegistrationForm, LoginForm

csrf = CSRFProtect()
auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/registration', methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username, password_hash=generate_password_hash(form.password))
        try:
            with Session(engine) as session:
                session.add(user)
                session.commit()
        except exc.SQLAlchemyError:
            return render_template('registration.html', reg_form=form)

        return redirect('/', code=302, Response=None)

    return render_template('registration.html', reg_form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/profile', code=302, Response=None)
    return render_template('login.html', login_form=form)
