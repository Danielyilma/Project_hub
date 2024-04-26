from project_hub import db
from flask_login import UserMixin
from project_hub.models.project import project_member
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(60))
    telegram = db.Column(db.String(60))
    linkedin = db.Column(db.String(60))
    #education
    #experiance
    #skills

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
        return f"user(<{self.full_nameu}>)"
