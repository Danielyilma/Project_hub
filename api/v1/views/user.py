from api.v1.views import app_views
from api.v1.app import db
from flask import request, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from project_hub.models.user import User, Skill
from jsonschema import ValidationError
from api.v1.views.obj_schema import serialize_user, validate_user, file_uploader
from http import HTTPStatus


@app_views.route('/user/sign-up', methods=['POST'], strict_slashes=False)
def user_registration():
    data = request.get_json()

    try:
        validate_user(data)
    except ValidationError as e:
        return make_response(jsonify({"Error" : e.message}), HTTPStatus.BAD_REQUEST)
    except AttributeError as e:
        return make_response(jsonify({"Error" : str(e)}), HTTPStatus.BAD_REQUEST)
    
    user = User()

    user.full_name= data.get("full_name", None)
    user.email= data.get("email", None)
    user.phone_number= data.get("phone_number", None)
    user.telegram=data.get("telegram", None)
    user.linkedin = data.get("linkedin", None)
    user.passwords = data.get("password", None)
    user.username = data.get("username", None)

    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify("Error"), HTTPStatus.BAD_REQUEST)

    return jsonify({"user": serialize_user(user)}), HTTPStatus.CREATED


@app_views.route("/user/login", methods=['POST'], strict_slashes=False)
def user_login():
    data = request.get_json()

    email = data.get('email', None)
    password = data.get('password', None)

    if not email and not password:
        return make_response({"Error": "email and password are required"}, HTTPStatus.BAD_REQUEST)
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response({"Error": "email not found"})
    elif not user.validate_password(password):
        return make_response({"Error": "Wrong password"})
    
    login_user(user)

    return jsonify("login successfull"), HTTPStatus.OK


@app_views.route("/user/logout", methods=["POST"], strict_slashes=False)
@login_required
def user_logout():
    logout_user()

    return jsonify("logout successfull"), HTTPStatus.OK


@app_views.route("/user", methods=['PUT'])
@login_required
def user_edit():
    data = request.get_json()

    update_attr = ["full_name", "phone_number", "telegram", "linkedin"]
    skills = data.get("skills", None)

    if "profile_pic" in request.files:
        file = request.files["profile_pic"]
        current_user.profile_pic = file_uploader(file)

    for key, value in data.items():
        if key in update_attr:
            setattr(current_user, key, value)

    if skills and not Skill.query.filter_by(name=skills, user_id=current_user.id):
        skill = Skill()
        skill.name = skills
        skill.user_id = current_user.id
        db.session.add(skill)
    
    db.session.add(current_user)
    db.session.commit()

    return jsonify({"user": serialize_user(current_user)}), HTTPStatus.OK


@app_views.route("/user/<int:id>", methods=['GET'], strict_slashes=False)
@login_required
def user_profile(id):
    user = User.query.get_or_404(id)

    return jsonify({"user": serialize_user(user)}), HTTPStatus.OK
