from sqlalchemy import or_
from project_hub import app, db
from project_hub.forms import RegistrationForm, LoginForm, ProjectCreationForm
from flask import render_template, redirect, url_for, make_response, abort, request
from project_hub.models.user import User
from flask_login import current_user, login_required, login_user, logout_user
from project_hub.models.project import Project, ProjectScreenShot
from werkzeug.utils import secure_filename
import uuid, os
from project_hub.models.request import Request
from project_hub.models.user import User

def file_uploader(file):
    file_name = secure_filename(file.filename)
    file_name = str(uuid.uuid1()) + "_" + file_name
    base_path = app.config['UPLOAD_FOLDER']
    file.save(os.path.join(app.root_path, base_path, file_name))
    return file_name

@app.route('/')
def landing():
    return render_template('index.html')


@app.route('/')
@app.route('/home')
@login_required
def home():
    return get_projects()

@app.route('/user/projects')
@login_required
def user_projects():
    projects = Project.query.filter_by(owner_id=current_user.id)
    return render_template('projects.html', projects=projects)



@app.route('/projects', methods=['GET'])
@login_required
def get_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/project/<int:id>', methods=['GET'])
@login_required
def get_project(id):
    project = Project.query.filter_by(id=id).first()
    visuals = ProjectScreenShot.query.filter_by(project_id=id).all()

    if project:
        return render_template('project.html', project=project, visuals=visuals)
    return abort(404)
        


@app.route('/project/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectCreationForm()

    if form.validate_on_submit():
        project = Project()

        project.name = form.name.data
        project.description = form.description.data
        project.project_link = form.project_link.data
        # project.is_public = form.is_public.data
        project.progress = "planning"
        project.owner_id = current_user.id

        file = request.files['banner']
        if file:
            project.banner = file_uploader(file)
        db.session.add(project)

        visuals = form.project_visual.data 
        visuals = [] if visuals is None else visuals

        for visual in visuals:
            Project_visual = ProjectScreenShot()
            Project_visual.screenshot = file_uploader(visual)
            Project_visual.project_id = Project.id
            db.session.add(Project_visual)

        db.session.commit()
        return redirect(url_for('get_projects'))

    return render_template('create_project.html', form=form)

@app.route('/project/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    form = ProjectCreationForm()
    project = Project.query.get_or_404(id)

    if project.owner != current_user:
        return abort(401)

    if request.method == 'GET':
        form.name.data = project.name
        form.description.data = project.description
        form.progress.data = project.progress
        form.project_link.data = project.project_link
    elif request.method == 'POST' and form.validate_on_submit:
        project.name = form.name.data
        project.description = form.description.data
        project.project_link = form.project_link.data
        # project.is_public = form.is_public.data
        project.progress = "planning"
        file = request.files['banner']
        if file:
            project.banner = file_uploader(file)
        db.session.add(project)

        visuals = form.project_visual.data 
        visuals = [] if visuals is None else visuals
        

        for visual in visuals:
            Project_visual = ProjectScreenShot()
            Project_visual.screenshot = file_uploader(visual)
            Project_visual.project_id = id
            db.session.add(Project_visual)

        db.session.commit()
        return get_project(id)    
    return render_template('create_project.html', form=form, project=project)
    



@login_required
@app.route('/request', methods=["POST"])
def request_for_project():
    if request.form.get('_method', None):
        id = request.form.get('request_id')
        request2 = Request.query.get_or_404(id)
        db.session.delete(request2)
    else:
        project_id = request.form.get('project_id')
        request1 = Request()
        request1.requester_id = current_user.id
        request1.recipient_id = Project.query.get_or_404(project_id).owner_id
        request1.project_id = project_id
        db.session.add(request1)
    db.session.commit()

    return redirect("/projects")


@login_required
@app.route('/accept/<int:id>', methods=["GET"])
def accept(id):
    request1 = Request.query.get_or_404(id)
    project = Project.query.get_or_404(request1.project_id)
    user = request1.requester
    request2 = Request()
    request2.requester_id = current_user.id
    request2.recipient_id = request1.requester_id
    request2.project_id = request1.project_id

    if request.args.get("accept", None):
        project.members.append(user)
        request2.reason = "you got accepted"
        db.session.add(request2)
    elif request.args.get("decline", None):
        request2.reason = "you got declined"
        db.session.add(request2)

    db.session.delete(request1)
    db.session.commit()
    return redirect("/projects")


