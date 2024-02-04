from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(message='This field is required'),
                                                Length(min=4, max=25, message='From 4 to 25 characters')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='This field is required')]
                             )
    password_confirm = PasswordField('Password Confirm',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords are not equal')])


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(message='Wrong login or password')])
    password = PasswordField('Password', validators=[DataRequired(message='Wrong login or password')])