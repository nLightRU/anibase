from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, EqualTo, Length, Email


class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(message='This field is required'),
                                             Length(min=4, max=25, message='From 4 to 25 characters')])
    email = StringField('Email')
    password = PasswordField('Password',
                             validators=[DataRequired(message='This field is required')]
                             )
    password_confirm = PasswordField('Password Confirm',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords are not equal')])

    birthday = DataRequired('Birthday')
