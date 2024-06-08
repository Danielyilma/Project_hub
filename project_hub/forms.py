from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField, TextAreaField, FileField, BooleanField
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from project_hub.models.user import User
import re

class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    bio = TextAreaField("")
    profile_pic = FileField("profile")
    telegram = StringField("Telegram")
    linkedin = StringField("Linkedin")
    submit = SubmitField("Submit")

    def validate_email(form, field):
        existing_user = User.query.filter_by(email=field.data).first()
        if existing_user:
            raise ValidationError('email already in use. Please choose a different one.')
    
    def validate_phone_number(form, field):
        if not re.match('\+?\d{10}', field.data):
            raise ValidationError('Wrong format, format must be (+251909008734)')


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ProjectCreationForm(FlaskForm):
    name = StringField('Project title', validators=[DataRequired()])
    description = TextAreaField('project description', validators=[DataRequired()])
    banner = FileField('Banner for the project', validators=[])
    project_visual = MultipleFileField("Project Visual Asset", validators=[FileAllowed(['jpg', 'png'])])
    progress = StringField('Progress')
    project_link = StringField('Project link', validators=[DataRequired()])
    is_public = BooleanField('Is public')
    submit = SubmitField("Create")