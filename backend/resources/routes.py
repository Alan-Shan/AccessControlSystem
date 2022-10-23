from datetime import datetime
from datetime import timedelta
from datetime import timezone


import flask
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

from database.model.token import TokenBlocklist
from database.model.admin import Admin
from database.db import db
from database.model.visitrequest import VisitRequest


# Login route
def login():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    username = flask.request.json.get('username', None)
    password = flask.request.json.get('password', None)
    if not username:
        return flask.jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400

    admin = Admin.query.filter_by(username=username).first()
    if admin.password != password or admin is None:
        return flask.jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_access_token(identity=username)
    return flask.jsonify(access_token=access_token, refresh_token=refresh_token), 200


def add_visit_request():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    visit_request = VisitRequest()
    visit_request.name = flask.request.json.get('name', None)
    visit_request.surname = flask.request.json.get('surname', None)
    visit_request.patronymic = flask.request.json.get('patronymic', None)
    visit_request.email = flask.request.json.get('email', None)
    visit_request.phone = flask.request.json.get('phone', None)
    visit_request.document_type = flask.request.json.get('document_type', None)
    visit_request.document_number = flask.request.json.get('document_number', None)
    visit_request.purpose = flask.request.json.get('purpose', None)

    db.session.add(visit_request)
    db.session.commit()

    # get id
    visit_request_id = visit_request.id

    return flask.jsonify({"msg": "Visit request added", "visit_request_id": visit_request_id}), 200


def get_not_approved_visit_requests():
    visit_requests = VisitRequest.query.filter_by(approved=False).all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


def get_approved_visit_request():
    visit_requests = VisitRequest.query.filter_by(approved=True).all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


def get_visit_requests_by_id():
    visit_request_id = flask.request.json.get('visit_request_id', None)
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    return flask.jsonify(visit_request.serialize()), 200


def approve_visit_request():
    visit_request_id = flask.request.json.get('visit_request_id', None)
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    visit_request.approved = True
    db.session.commit()
    return flask.jsonify({"msg": "Visit request approved"}), 200


def reject_visit_request():
    visit_request_id = flask.request.json.get('visit_request_id', None)
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    visit_request.approved = False
    db.session.commit()
    return flask.jsonify({"msg": "Visit request rejected"}), 200


@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    modify_token()
    access_token = create_access_token(identity=identity, fresh=False)
    return flask.jsonify(access_token=access_token)


# protected route
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return flask.jsonify(logged_in_as=current_user), 200


# logout route
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return flask.jsonify(msg="JWT revoked")


def init_routes(app):
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/refresh', 'refresh', refresh, methods=['POST'])
    app.add_url_rule('/protected', 'protected', protected, methods=['GET'])
    app.add_url_rule('/logout', 'logout', modify_token, methods=['DELETE'])
    app.add_url_rule('/add_request', 'add_visit_request', add_visit_request, methods=['POST'])
    app.add_url_rule('/get_not_approved_requests', 'get_not_approved_visit_requests', get_not_approved_visit_requests, methods=['GET'])
    app.add_url_rule('/get_approved_requests', 'get_approved_visit_request', get_approved_visit_request, methods=['GET'])
    app.add_url_rule('/get_request', 'get_visit_requests_by_id', get_visit_requests_by_id, methods=['POST'])
    app.add_url_rule('/approve_request', 'approve_visit_request', approve_visit_request, methods=['POST'])
    app.add_url_rule('/reject_request', 'reject_visit_request', reject_visit_request, methods=['POST'])
