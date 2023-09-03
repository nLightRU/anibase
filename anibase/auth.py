import flask
from flask import Blueprint, render_template
from flask import redirect
from flask_wtf import CSRFProtect

from .forms import RegisterForm

csrf = CSRFProtect()
auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/registration', methods=['GET', 'POST'])
def registration_page():
    form = RegisterForm()
    if form.validate_on_submit():

        return redirect('/', code=302, Response=None)
    return render_template('registration.html', reg_form=form)
