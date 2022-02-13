from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class LogInForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    rememberMe = BooleanField('rememberMe')

class SignUpForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('passwordCheck', message='password mismatch')])
    passwordCheck = PasswordField('passwordCheck', validators=[DataRequired()])