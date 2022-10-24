import os
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
from database.model.image_counter import ImageCounter

import re


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
    # get image from request
    image = flask.request.files['image']
    if image.filename:
        name = str(ImageCounter.query.first().counter)
        image.save('images/profile_pic' + name + '.jpg')
        ImageCounter.query.first().counter += 1
        db.session.commit()
        visit_request.image = name + '.jpg'

    visit_request.name = flask.request.json.get('name', None)
    visit_request.surname = flask.request.json.get('surname', None)
    visit_request.patronymic = flask.request.json.get('patronymic', None)
    visit_request.email = flask.request.json.get('email', None)
    visit_request.phone = flask.request.json.get('phone', None)
    visit_request.document_type = flask.request.json.get('document_type', None)
    visit_request.document_number = flask.request.json.get('document_number', None)
    visit_request.purpose = flask.request.json.get('purpose', None)

    if not visit_request.name:
        return flask.jsonify({"msg": "Missing name parameter"}), 400
    if not visit_request.surname:
        return flask.jsonify({"msg": "Missing surname parameter"}), 400
    if not visit_request.patronymic:
        return flask.jsonify({"msg": "Missing patronymic parameter"}), 400
    if not visit_request.email:
        return flask.jsonify({"msg": "Missing email parameter"}), 400
    if not visit_request.phone:
        return flask.jsonify({"msg": "Missing phone parameter"}), 400
    if not visit_request.document_type:
        return flask.jsonify({"msg": "Missing document_type parameter"}), 400
    if not visit_request.document_number:
        return flask.jsonify({"msg": "Missing document_number parameter"}), 400
    if not visit_request.purpose:
        return flask.jsonify({"msg": "Missing purpose parameter"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", visit_request.email):
        return flask.jsonify({"msg": "Invalid email"}), 400
    if not re.match(r"^\+?3?8?(0\d{9})$", visit_request.phone):
        return flask.jsonify({"msg": "Invalid phone"}), 400
    if len(visit_request.document_number) != 10:
        return flask.jsonify({"msg": "Invalid document number"}), 400

    # check if visit request with this email already exists
    if VisitRequest.query.filter_by(email=visit_request.email).first() is not None:
        return flask.jsonify({"msg": "Visit request with this email already exists"}), 400
    # check if visit request with this phone already exists
    if VisitRequest.query.filter_by(phone=visit_request.phone).first() is not None:
        return flask.jsonify({"msg": "Visit request with this phone already exists"}), 400
    # check if visit request with this document number already exists
    if VisitRequest.query.filter_by(document_number=visit_request.document_number).first() is not None:
        return flask.jsonify({"msg": "Visit request with this document number already exists"}), 400

    db.session.add(visit_request)
    db.session.commit()

    # get id
    visit_request_id = visit_request.id

    return flask.jsonify({"msg": "Visit request added", "visit_request_id": visit_request_id}), 200


@jwt_required()
def get_visit_requests():
    visit_requests = VisitRequest.query.all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


@jwt_required()
def get_not_approved_visit_requests():
    visit_requests = VisitRequest.query.filter_by(approved=False).all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


@jwt_required()
def get_approved_visit_request():
    visit_requests = VisitRequest.query.filter_by(approved=True).all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


@jwt_required()
def get_visit_requests_by_id():
    visit_request_id = flask.request.json.get('visit_request_id', None)
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    return flask.jsonify(visit_request.serialize()), 200


@jwt_required()
def approve_visit_request():
    visit_request_id = flask.request.json.get('visit_request_id', None)
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    visit_request.approved = True
    db.session.commit()
    return flask.jsonify({"msg": "Visit request approved"}), 200


@jwt_required()
def reject_visit_request():
    visit_request_id = flask.request.json.get('visit_request_id', None)
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    visit_request.approved = False
    db.session.commit()
    return flask.jsonify({"msg": "Visit request rejected"}), 200


@jwt_required()
def add_picture():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400
    visit_request_id = flask.request.json.get('visit_request_id', None)

    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    image = flask.request.files['image']

    if not image.filename:
        return flask.jsonify({"msg": "Missing image parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if visit_request is None:
        return flask.jsonify({"msg": "Visit request not found"}), 404

    if image.filename:
        name = str(ImageCounter.query.first().counter)
        image.save('images/profile_pic' + name + '.jpg')
        ImageCounter.query.first().counter += 1
        visit_request.image = name + '.jpg'
        db.session.commit()

    return flask.jsonify({"msg": "Image added"}), 200


@jwt_required()
def get_picture_by_id():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400
    visit_request_id = flask.request.json.get('visit_request_id', None)

    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if visit_request is None:
        return flask.jsonify({"msg": "Visit request not found"}), 404

    if visit_request.image is None:
        return flask.jsonify({"msg": "Image not found"}), 404

    return flask.send_file('images/profile_pic' + visit_request.image)


@jwt_required()
def get_picture_by_patch():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400
    image_patch = flask.request.json.get('image_patch', None)
    if not image_patch:
        return flask.jsonify({"msg": "Missing image_patch parameter"}), 400

    if not os.path.isfile('images/profile_pic' + image_patch):
        return flask.jsonify({"msg": "Image not found"}), 404

    return flask.send_file('images/profile_pic' + image_patch)


@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    modify_token()
    access_token = create_access_token(identity=identity, fresh=False)
    return flask.jsonify(access_token=access_token)


@jwt_required()
def who_iam():
    identity = get_jwt_identity()
    return flask.jsonify(logged_in_as=identity), 200


# logout route
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return flask.jsonify(msg="JWT revoked")


@jwt_required()
def add_admin():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "supper_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 400

    admin = Admin()
    admin.username = flask.request.json.get('username', None)
    admin.password = flask.request.json.get('password', None)
    if not admin.username:
        return flask.jsonify({"msg": "Missing username parameter"}), 400
    if not admin.password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400

    # check if admin with this username already exists
    if Admin.query.filter_by(username=admin.username).first():
        return flask.jsonify({"msg": "Admin with this username already exists"}), 400

    db.session.add(admin)
    db.session.commit()

    return flask.jsonify({"msg": "Admin added"}), 200


@jwt_required()
def get_admins():
    admins = Admin.query.all()
    return flask.jsonify([admin.serialize() for admin in admins]), 200


@jwt_required()
def get_admin_by_id():
    admin_id = flask.request.json.get('admin_id', None)
    admin = Admin.query.filter_by(id=admin_id).first()
    return flask.jsonify(admin.serialize()), 200


@jwt_required()
def delete_admin():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "supper_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 400

    admin_id = flask.request.json.get('admin_id', None)

    if not admin_id:
        return flask.jsonify({"msg": "Missing admin_id parameter"}), 400

    admin = Admin.query.filter_by(id=admin_id).first()

    # check if admin with this id exists
    if not admin:
        return flask.jsonify({"msg": "Admin with this id does not exists"}), 400

    db.session.delete(admin)
    db.session.commit()
    return flask.jsonify({"msg": "Admin deleted"}), 200


@jwt_required()
def change_admin_type():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "supper_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 400

    admin_id = flask.request.json.get('admin_id', None)
    admin_type = flask.request.json.get('admin_type', None)
    if not admin_id:
        return flask.jsonify({"msg": "Missing admin_id parameter"}), 400
    if not admin_type:
        return flask.jsonify({"msg": "Missing admin_type parameter"}), 400

    admin = Admin.query.filter_by(id=admin_id).first()
    admin.admin_type = admin_type
    db.session.commit()
    return flask.jsonify({"msg": "Admin type changed"}), 200


def init_routes(app):
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/refresh', 'refresh', refresh, methods=['POST'])
    app.add_url_rule('/who_iam', 'who_iam', who_iam, methods=['GET'])
    app.add_url_rule('/logout', 'logout', modify_token, methods=['DELETE'])
    app.add_url_rule('/add_request', 'add_visit_request', add_visit_request, methods=['POST'])
    app.add_url_rule('/get_requests', 'get_visit_requests', get_visit_requests, methods=['GET'])
    app.add_url_rule('/add_picture', 'add_picture', add_picture, methods=['POST'])
    app.add_url_rule('/get_picture_by_id', 'get_picture_by_id', get_picture_by_id, methods=['GET'])
    app.add_url_rule('/get_picture_by_patch', 'get_picture_by_patch', get_picture_by_patch, methods=['GET'])
    app.add_url_rule('/get_not_approved_requests', 'get_not_approved_visit_requests', get_not_approved_visit_requests, methods=['GET'])
    app.add_url_rule('/get_approved_requests', 'get_approved_visit_request', get_approved_visit_request, methods=['GET'])
    app.add_url_rule('/get_request', 'get_visit_requests_by_id', get_visit_requests_by_id, methods=['POST'])
    app.add_url_rule('/approve_request', 'approve_visit_request', approve_visit_request, methods=['POST'])
    app.add_url_rule('/reject_request', 'reject_visit_request', reject_visit_request, methods=['POST'])
    app.add_url_rule('/add_admin', 'add_admin', add_admin, methods=['POST'])
    app.add_url_rule('/get_admins', 'get_admins', get_admins, methods=['GET'])
    app.add_url_rule('/get_admin', 'get_admin_by_id', get_admin_by_id, methods=['POST'])
    app.add_url_rule('/delete_admin', 'delete_admin', delete_admin, methods=['POST'])
    app.add_url_rule('/change_admin_type', 'change_admin_type', change_admin_type, methods=['POST'])
