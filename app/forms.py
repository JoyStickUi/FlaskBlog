from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_security.forms import RegisterForm, LoginForm


class ExtendedRegisterForm(RegisterForm):
	email = StringField('email', validators=[Email(), DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])