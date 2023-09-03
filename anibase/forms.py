from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
