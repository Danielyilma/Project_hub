from datetime import datetime
from project_hub import db

project_member = db.Table(
    'project_member',
    db.Column('Project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    descriptions = db.Column(db.Text)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    banner = db.Column(db.String(60))
    #progress
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    screen_shots = db.relationship('ProjectScreenShot', backref='project')
    members = db.relationship('User', secondary='project_member', back_populates='projects')



class ProjectScreenShot(db.Model):
    __tablename__ = 'project_screenshot'
    id = db.Column(db.Integer, primary_key=True)
    screenshot = db.Column(db.String(60))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

