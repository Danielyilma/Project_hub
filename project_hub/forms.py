from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name:", validators=[DataRequired()])
    email = EmailField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    phone_number = StringField("Phone Number:", validators=[DataRequired()])
    telegram = StringField("Telegram:")
    linkedin = StringField("Linkedin:")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = EmailField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")