from project_hub import db, app
from project_hub.models.project import Project, ProjectScreenShot, project_member
from project_hub.models.request import Request
from project_hub.models.user import User, Skill

if __name__ == '__main__':
    db.create_all()