from project_hub import db
from flask_login import UserMixin
from project_hub.models.project import project_member
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(60), unique=True, nullable=False)
    profile_pic = db.Column(db.String(60), default='test')
    password = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(60))
    telegram = db.Column(db.String(60))
    linkedin = db.Column(db.String(60))
    bio = db.Column(db.Text)
    #education
    #experiance
    skills = db.relationship('Skill', backref='user')
    requests = db.relationship('Request', foreign_keys='Request.recipient_id')
    projects = db.relationship('Project', secondary='project_member')

    @property
    def passwords(self):
        return self.password

    @passwords.setter
    def passwords(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"user(<{self.full_name}>)"


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
