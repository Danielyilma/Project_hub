from api.v1.app import db, app
from sqlalchemy import or_
from flask import url_for
from jsonschema import validate
from project_hub.models.user import User, Skill
from project_hub.models.project import ProjectScreenShot
from werkzeug.utils import secure_filename
import uuid, os

UserSchema = {
    "type": "object",
    "properties": {
        "full_name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "phone_number" : {"type": "string"},
        "telegram" : {"type": "string"},
        "linkedin" : {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required" : ["full_name", "username", "password", "email", "phone_number"]
}

ProjectSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "project_link" : {"type": "string"}
    },
    "required" : ["name", "description", "project_link"]
}

# RequestSchema = {
#     "type": "object",
#     "properties": {
#         "reason": {"type": "string"},
#         "requester_id": {"type": "integer"},
#         "project_id" : {"type": "integer"}
#     },
#     "required": ["reason", "project_id"]
# }

def serialize_user(user):
    skills = [sk.name for sk in Skill.query.filter_by(id=user.id).all()]

    hidden = ['_sa_instance_state', 'password'] 

    user_dict = user.__dict__

    del user_dict['_sa_instance_state'], user_dict['password']

    return user_dict

def serialize_project(project):
    visuals = [visual.screenshot for visual in 
               ProjectScreenShot.query.filter_by(project_id=project.id).all()]
    
    project_dict = project.__dict__

    project_dict['visuals'] = visuals

    del project_dict['_sa_instance_state']

    return project_dict

def serialize_request(req):
    request_dict = {
        'id': req.id,
        'project_id': req.project_id,
        'requester_id': req.requester_id,
        'recipient_id': req.recipient_id,
        'reason': req.reason
    }

    return request_dict

def validate_user(data):
    validate(data, UserSchema)
    
    if User.query.filter_by(username=data["username"]).all():
        raise AttributeError("username already exists")
    elif User.query.filter_by(email=data["email"]).all():
        print("hello")
        raise AttributeError("email aleady exists")

    
def file_uploader(file):
    file_name = secure_filename(file.filename)
    file_name = str(uuid.uuid1()) + "_" + file_name
    base_path = app.config['UPLOAD_FOLDER']
    file.save(os.path.join(app.root_path, base_path, file_name))
    return file_name


def delete_uploaded_file(filename):
    root = app.root_path
    path = root + url_for('static', filename='images/') + filename
    try:
        os.remove(path)
    except Exception as e:
        return None