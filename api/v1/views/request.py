from api.v1.views import app_views, db
from flask import jsonify, make_response, request, abort
from flask_login import current_user, login_required
from http import HTTPStatus
from api.v1.views.obj_schema import serialize_request
from project_hub.models.request import Request
from project_hub.models.user import User
from project_hub.models.project import Project

@app_views.route("/projects/request", methods=['POST'], strict_slashes=False)
@login_required
def create_request():
    data = request.form.to_dict()

    if "project_id" not in data.keys():
        return make_response(jsonify({"Error": "project_id is required"}), 400)

    req = Request()

    req.reason = data.get("reason")
    req.project_id = int(data.get("project_id"))
    req.requester_id = current_user.id

    project = Project.query.get_or_404(req.project_id)
    req.recipient_id = User.query.get_or_404(project.owner_id).id

    db.session.add(req)
    db.session.commit()

    return jsonify({"request": serialize_request(req)}), HTTPStatus.OK


@app_views.route("/projects/request", methods=['DELETE'], strict_slashes=False)
@login_required
def delete_request():
    id = request.form.get("id")

    if not id:
        make_response(jsonify({"Error": "id required"}))
    
    req = Request.query.get_or_404(id)

    if req.recipient_id != current_user.id:
        return abort(401)
    
    db.session.delete(req)
    db.session.commit()

    return jsonify("request deleted successfull"), HTTPStatus.OK


@app_views.route("/projects/request", methods=['GET'], strict_slashes=False)
@login_required
def get_user_requests():
    requests = Request.query.filter_by(recipient_id=current_user.id).all()

    requestsli = []

    for req in requests:
        requestsli.append(serialize_request(req))
    
    return jsonify({"requests": requestsli}), HTTPStatus.OK


