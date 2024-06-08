from api.v1.views import app_views, db
from flask import jsonify, request, make_response, abort
from flask_login import current_user, login_required
from jsonschema import validate, ValidationError
from api.v1.views.obj_schema import ProjectSchema, file_uploader, serialize_project, delete_uploaded_file
from http import HTTPStatus
from project_hub.models.project import Project, ProjectScreenShot

@app_views.route("/projects", methods=['POST'], strict_slashes=False)
@login_required
def create_project():
    data = request.form.to_dict()

    try:
        validate(data, ProjectSchema)
    except ValidationError as e:
        return make_response({"Error": e.message}, HTTPStatus.BAD_REQUEST)

    project = Project()
    project.name = data['name']
    project.description = data['description']
    project.project_link = data['project_link']
    project.owner_id = current_user.id

    file = request.files.get('banner', None)
    if file:
        project.banner = file_uploader(file)

    db.session.add(project)
    db.session.commit()

    visuals = request.files.getlist('visuals', None)
    visuals = [] if visuals is None else visuals

    for visual in visuals:
        Project_visual = ProjectScreenShot()
        Project_visual.screenshot = file_uploader(visual)
        Project_visual.project_id = project.id
        db.session.add(Project_visual)

    db.session.commit()
    return jsonify({"project": serialize_project(project)}), HTTPStatus.CREATED


@app_views.route("/projects/<int:id>", methods=['PUT'], strict_slashes=False)
@login_required
def update_projects(id):
    project = Project.query.get_or_404(id)

    if project.owner != current_user:
        abort(401)

    data = request.form.to_dict()

    update_attr = ['name', 'description', 'project_link']

    for key, value in data.items():
        if key in update_attr:
            setattr(project, key, value)
    
    file = request.files['banner']
    if file:
        delete_uploaded_file(project.banner)
        project.banner = file_uploader(file)
    
    visuals = request.files.getlist("visuals")
    visuals = [] if visuals is None else visuals

    for visual in visuals:
        Project_visual = ProjectScreenShot()
        Project_visual.screenshot = file_uploader(visual)
        Project_visual.project_id = id
        db.session.add(Project_visual)

    db.session.commit()
    return jsonify({"project": serialize_project(project)}), HTTPStatus.OK


@app_views.route("/projects", methods=['GET'], strict_slashes=False)
@login_required
def get_projects():
    projects = Project.query.all()

    projectsli = []
    for project in projects:
        projectsli.append(serialize_project(project))

    return jsonify({"projects": projectsli}), 200


@app_views.route("/projects/<int:id>", methods=['GET'], strict_slashes=False)
def get_project(id):
    project = Project.query.filter_by(id=id).first()

    return jsonify({"project": serialize_project(project)}), 200