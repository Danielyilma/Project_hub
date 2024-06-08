from project_hub import app, db
from project_hub.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, request, abort
from project_hub.models.user import User, Skill
from flask_login import login_required, login_user, logout_user, current_user
from project_hub.models.views.projects import file_uploader, delete_uploaded_file
from project_hub.models.project import Project


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()

        user.full_name=form.full_name.data
        user.email=form.email.data
        user.phone_number=form.phone_number.data
        user.telegram=form.telegram.data
        user.linkedin = form.linkedin.data
        user.passwords = form.password.data
        user.username = form.username.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('sign_up.html', form=form)




@app.route("/edit/<int:id>", methods=['POST', 'GET'])
@login_required
def edit_profile(id):
    form = RegistrationForm()

    if id != current_user.id:
        return abort(404)
    if request.method == "POST":
        if "profile_pic" in request.files:
            file = request.files["profile_pic"]

            if file:
                delete_uploaded_file(current_user.profile_pic)
                current_user.profile_pic = file_uploader(file)
        else:
            skills = request.form.get('skills')

            if not Skill.query.filter_by(name=skills, user_id=current_user.id).first():
                skill = Skill()
                skill.name = skills
                skill.user_id = current_user.id
                db.session.add(skill)

            current_user.full_name = form.full_name.data
            current_user.email=form.email.data
            current_user.phone_number=form.phone_number.data
            current_user.telegram=form.telegram.data
            current_user.linkedin = form.linkedin.data
            current_user.username = form.username.data
            current_user.bio = form.bio.data
        
        db.session.add(current_user)
        db.session.commit()
    else:
        form.bio.data = current_user.bio

    return render_template("profile_edit.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user and user.validate_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    
    return render_template('login.html', form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing"))


@app.route("/profile", methods=["GET"])
@login_required
def get_profile():
    skills = Skill.query.filter(Skill.user_id==current_user.id).all()

    projects = Project.query.filter_by(owner_id=current_user.id).all()

    return render_template("profile.html", skills=skills, current_user=current_user, projects=projects)

@app.route("/profile/<int:id>", methods=["GET"])
@login_required
def get_user_profile(id):
    skills = Skill.query.filter(Skill.user_id==id).all()
    user = User.query.get_or_404(id)

    return render_template("profile.html", skills=skills, current_user=user, only_view=True)