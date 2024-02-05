import flask
from flask import Blueprint, render_template, request, url_for
from flask import redirect

from flask_login import LoginManager, login_user, login_required, logout_user

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.orm import Session

from .model import engine, User
from .forms import RegistrationForm, LoginForm

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    with Session(engine) as session:
        return session.get(User, user_id)


auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, password=form.password.data)
            # flask.flash(f"{form.username.data}, {form.password.data}")
            try:
                with Session(engine) as session:
                    session.add(user)
                    session.commit()
            except SQLAlchemyError:
                return render_template('signup.html', reg_form=form)
        return redirect(url_for('views.index'))

    return render_template('signup.html', reg_form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with Session(engine) as session:
            try:
                stmt = select(User).where(User.username == form.username.data)
                user = session.execute(stmt).scalar_one()
                if user is not None and user.verify_password(form.password.data):
                    login_user(user)
                    return render_template('profile.html', user=user)
                    # return redirect(request.args.get('next'))
            except NoResultFound:
                redirect("login.html", code=302, Response=None)

    return render_template('login.html', login_form=form)


@auth.route('logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('views.index'))
