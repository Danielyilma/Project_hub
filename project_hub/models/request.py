from datetime import datetime
from project_hub import db

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    reason = db.Column(db.Text)
    requester = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
