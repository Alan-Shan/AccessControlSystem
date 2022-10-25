import base64
import os
from datetime import datetime
from datetime import timezone


import flask
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import decode_token

from database.model.token import TokenBlocklist
from database.model.admin import Admin
from database.db import db
from database.model.visitrequest import VisitRequest
from database.model.image_counter import ImageCounter

import re


# Login route
def login():
    """
    Login route
    Call this route to get a JWT token to be used with the other protected routes
    ---
    tags:
        - auth
    parameters:
     - name: body
       in: body
       schema:
                type: object
                properties:
                    username:
                        type: string
                    password:
                        type: string
    responses:
        200:
            description: Login successful
            schema:
                type: object
                properties:
                    access_token:
                        type: string
                    refresh_token:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
    """
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    username = flask.request.json.get('username', None)
    password = flask.request.json.get('password', None)
    if not username:
        return flask.jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400

    admin = Admin.query.filter_by(username=username).first()
    if admin is None or admin.password != password:
        return flask.jsonify({"msg": "Bad username or password"}), 401

    # blocklist all tokens from a user when he logs in
    tokens = (admin.access_token, admin.refresh_token)
    for token in tokens:
        if token is not None and token != '':
            token = decode_token(token, csrf_value=None, allow_expired=True)
            jti = token['jti']
            ttype = token['type']
            now = datetime.now(timezone.utc)
            db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
            db.session.commit()

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    admin.access_token = access_token
    admin.refresh_token = refresh_token
    db.session.commit()

    return flask.jsonify(access_token=access_token, refresh_token=refresh_token), 200


def add_visit_request():
    """
    Add visit request
    Call this route to add a visit request
---
    tags:
        - visit_request
    parameters:
     - in: body
       name: body
       schema:
                type: object
                properties:
                    name:
                        type: string
                    surname:
                        type: string
                    phone:
                        type: string
                    email:
                        type: string
                    date:
                        type: string
                    time:
                        type: string
                    description:
                        type: string
    responses:
        200:
            description: Visit request added
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
    """
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    visit_request = VisitRequest()
    # get image from request
    image = flask.request.json.get('base64_image', None)
    if image:
        image_from_base64 = base64.b64decode(image)
        name = str(ImageCounter.query.first().counter) + '.jpg'
        ImageCounter.query.first().counter += 1
        db.session.commit()
        with open('images/profile_pic/' + name, "wb") as f:
            f.write(image_from_base64)
        visit_request.image = name
        db.session.commit()

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
    # check if phone number is valid (Russian phone number) (+79999999999) or (89999999999)
    if not re.match(r"^\+?7?8?\d{10}$", visit_request.phone):
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
    """
    Get visit requests
    Call this route to get all visit requests (only for admins)
    ---
    security:
        - bearerAuth: []
    tags:
        - visit_request
    responses:
        200:
            description: Visit requests
            schema:
                type: object
                properties:
                    visit_requests:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                name:
                                    type: string
                                surname:
                                    type: string
                                patronymic:
                                    type: string
                                email:
                                    type: string
                                phone:
                                    type: string
                                document_type:
                                    type: string
                                document_number:
                                    type: string
                                purpose:
                                    type: string
                                image:
                                    type: string (image path) may be null
        401:
            description: Login failed
    """
    visit_requests = VisitRequest.query.all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


@jwt_required()
def get_not_approved_visit_requests():
    """
    Get not approved visit requests
    Call this route to get all not approved visit requests (only for admins)
    ---
    tags:
        - visit_request
    security:
        - bearerAuth: []
    responses:
        200:
            description: Visit requests
            schema:
                type: object
                properties:
                    visit_requests:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                name:
                                    type: string
                                surname:
                                    type: string
                                patronymic:
                                    type: string
                                email:
                                    type: string
                                phone:
                                    type: string
                                document_type:
                                    type: string
                                document_number:
                                    type: string
                                purpose:
                                    type: string
                                image:
                                    type: string (image path) may be null
        401:
            description: Login failed
    """
    visit_requests = VisitRequest.query.filter_by(status="rejected").all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


@jwt_required()
def get_approved_visit_request():
    """
    Get approved visit requests
    Call this route to get all approved visit requests (only for admins)
    ---
    security:
        - bearerAuth: []
    tags:
        - visit_request
    responses:
        200:
            description: Visit requests
            schema:
                type: object
                properties:
                    visit_requests:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                name:
                                    type: string
                                surname:
                                    type: string
                                patronymic:
                                    type: string
                                email:
                                    type: string
                                phone:
                                    type: string
                                document_type:
                                    type: string
                                document_number:
                                    type: string
                                purpose:
                                    type: string
                                image:
                                    type: string (image path) may be null
        401:
            description: Login failed
    """
    visit_requests = VisitRequest.query.filter_by(status="approved").all()
    return flask.jsonify([visit_request.serialize() for visit_request in visit_requests]), 200


@jwt_required()
def get_visit_requests_by_id(id):
    """
    Get visit requests by id
    Call this route to get visit requests by id (only for admins)
    ---
    security:
        - bearerAuth: []
    tags:
        - visit_request
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: Visit request id
    responses:
        200:
            description: Visit requests
            schema:
                type: object
                properties:
                    visit_requests:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                name:
                                    type: string
                                surname:
                                    type: string
                                patronymic:
                                    type: string
                                email:
                                    type: string
                                phone:
                                    type: string
                                document_type:
                                    type: string
                                document_number:
                                    type: string
                                purpose:
                                    type: string
                                image:
                                    type: string (image path) may be null
        401:
            description: Login failed
    """
    visit_request_id = id
    if visit_request_id is None:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if visit_request is None:
        return flask.jsonify({"msg": "Visit request with this id does not exist"}), 400
    return flask.jsonify(visit_request.serialize()), 200


@jwt_required()
def approve_visit_request():
    """
    Approve visit request
    Call this route to approve visit request (only for admins)
    ---
    security:
        - bearerAuth: []
    tags:
        - visit_request
    parameters:
        - name: body
          in: body
          schema:
                type: object
                properties:
                    id:
                        type: integer
    responses:
        200:
            description: Visit request approved
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters) or visit request not found
        401:
            description: Login failed
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    visit_request_id = flask.request.json.get('id', None)
    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if not visit_request:
        return flask.jsonify({"msg": "Visit request not found"}), 400
    visit_request.status = 'approved'
    db.session.commit()
    return flask.jsonify({"msg": "Visit request approved"}), 200


@jwt_required()
def reject_visit_request():
    """
    Reject visit request
    Call this route to reject visit request (only for admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - visit_request
    parameters:
        - name: body
          in: body
          schema:
                type: object
                properties:
                    id:
                        type: integer
    responses:
        200:
            description: Visit request rejected
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters) or visit request not found
        401:
            description: Login failed
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    visit_request_id = flask.request.json.get('id', None)

    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if not visit_request:
        return flask.jsonify({"msg": "Visit request not found"}), 400
    visit_request.status = "rejected"
    db.session.commit()
    return flask.jsonify({"msg": "Visit request rejected"}), 200


@jwt_required()
def delete_visit_request():
    """
    Delete visit request
    Call this route to delete visit request (only for admins)
    ---
    security:
        - bearerAuth: []
    tags:
        - visit_request
    parameters:
        - name: body
          in: body
          schema:
                type: object
                properties:
                    id:
                        type: integer
    responses:
        200:
            description: Visit request deleted
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters) or visit request not found
        401:
            description: Login failed
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    visit_request_id = flask.request.json.get('id', None)
    if visit_request_id is None:
        return flask.jsonify({"msg": "Visit request id is not specified"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if visit_request is None:
        return flask.jsonify({"msg": "Visit request not found"}), 400

    db.session.delete(visit_request)
    db.session.commit()
    return flask.jsonify({"msg": "Visit request deleted"}), 200


@jwt_required()
def add_picture():
    """
    Add picture
    Call this route to add picture (only for admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - picture
    parameters:
        - name: body
          in : body
          schema:
                type: object
                properties:
                    base64_image:
                        type: string
                        description: base64 encoded image
                    id:
                        type: integer
    responses:
        200:
            description: Picture added
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        404:
            description: Visit request not found
    """
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400
    visit_request_id = flask.request.json.get('id', None)

    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    image = flask.request.json.get('base64_image', None)
    if not image:
        return flask.jsonify({"msg": "Missing base64_image parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if visit_request is None:
        return flask.jsonify({"msg": "Visit request not found"}), 404

    image_from_base64 = base64.b64decode(image)
    name = str(ImageCounter.query.first().counter) + '.jpg'
    ImageCounter.query.first().counter += 1
    db.session.commit()
    with open('images/profile_pic/' + name, "wb") as f:
        f.write(image_from_base64)
    visit_request.image = name
    db.session.commit()

    return flask.jsonify({"msg": "Image added"}), 200


@jwt_required()
def get_picture_by_id(id):
    """
    Get picture by id
    Call this route to get picture by id (only for admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - picture
    parameters:
        - name: id
          in: path
          type: integer
          required: true
    responses:
        200:
            description: Ok
            content:
                image/jpeg:
                    type: image
                    format: binary
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        404:
            description: Visit request not found or picture not found
    """
    visit_request_id = id
    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if visit_request is None:
        return flask.jsonify({"msg": "Visit request not found"}), 404

    if visit_request.image is None:
        return flask.jsonify({"msg": "Image not found"}), 404

    return flask.send_file('images/profile_pic' + visit_request.image, mimetype='image/jpg', as_attachment=True)


@jwt_required()
def get_picture_by_patch(patch):
    """
    Get picture by patch
    Call this route to get picture by patch (only for admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - picture
    parameters:
        - name: patch
          in: path
          type: string
          required: true
    responses:
        200:
            description: Ok
            content:
                image/jpeg:
                    type: image
                    format: binary
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        404:
            description: Picture not found
    """
    image_patch = patch
    if not image_patch:
        return flask.jsonify({"msg": "Missing image_patch parameter"}), 400

    if not os.path.isfile('images/profile_pic' + image_patch):
        return flask.jsonify({"msg": "Image not found"}), 404

    return flask.send_file('images/profile_pic' + image_patch, mimetype='image/jpg', as_attachment=True)


@jwt_required(refresh=True)
def refresh():
    """
    Refresh token
    Call this route to refresh token (only for admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - auth
    responses:
        200:
            description: Token refreshed
            schema:
                type: object
                properties:
                    access_token:
                        type: string
        401:
            description: Login failed
    """
    identity = get_jwt_identity()

    admin = Admin.query.filter_by(username=identity).first()

    token = decode_token(admin.access_token, csrf_value=None, allow_expired=True)
    jti = token['jti']
    ttype = token['type']
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
    db.session.commit()

    access_token = create_access_token(identity=identity)

    admin.access_token = access_token
    db.session.commit()

    return flask.jsonify(access_token=access_token)


@jwt_required()
def who_i_am():
    """
    Who iam
    Call this route to get admin info (only for admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - auth
    responses:
        200:
            description: Admin info
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    username:
                        type: string
                    role:
                        type: string
        401:
            description: Login failed
    """
    identity = get_jwt_identity()
    admin = Admin.query.filter_by(username=identity).first()
    return flask.jsonify(id=admin.id, username=admin.username, role=admin.admin_type), 200


# logout route
@jwt_required()
def modify_token():
    """
    logout
    Call this route to Log out (only for admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - auth
    responses:
        200:
            description: Token modified *logout*
            schema:
                type: object
                properties:
                    msg:
                        type: string
        401:
            description: Login failed
    """
    identity = get_jwt_identity()

    admin = Admin.query.filter_by(username=identity).first()
    for token in (admin.access_token, admin.refresh_token):
        token = decode_token(token, csrf_value=None, allow_expired=True)
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
        db.session.commit()

    return flask.jsonify(msg=f"{ttype.capitalize()} token successfully revoked"), 200


@jwt_required()
def add_admin():
    """
    Add admin
    Call this route to add admin (only for super admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - admin_management
    parameters:
        - name: body
          in: body
          schema:
                type: object
                properties:
                    username:
                        type: string
                    password:
                        type: string
                    admin_type:
                        type: string
    responses:
        200:
            description: Admin added
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        403:
            description: Permission denied
        409:
            description: Admin already exists
    """
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "super_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 403

    admin = Admin()
    admin.username = flask.request.json.get('username', None)
    admin.password = flask.request.json.get('password', None)
    admin.admin_type = flask.request.json.get('admin_type', None)
    if not admin.username:
        return flask.jsonify({"msg": "Missing username parameter"}), 400
    if not admin.password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400
    if not admin.admin_type:
        return flask.jsonify({"msg": "Missing admin_type parameter"}), 400

    # check if admin with this username already exists
    if Admin.query.filter_by(username=admin.username).first():
        return flask.jsonify({"msg": "Admin with this username already exists"}), 409

    db.session.add(admin)
    db.session.commit()

    return flask.jsonify({"msg": "Admin added"}), 200


@jwt_required()
def get_admins():
    """
    Get admins
    Call this route to get all admins (only for super admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - admin_management
    responses:
        200:
            description: Admins
            schema:
                type: object
                properties:
                    admins:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                username:
                                    type: string
                                role:
                                    type: string
        400:
            description:
        401:
            description: Login failed
        403:
            description: Permission denied
        404:
            description: Admin not found
    """
    # check if current user is supper admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "super_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 403
    admins = Admin.query.all()
    return flask.jsonify([admin.serialize() for admin in admins]), 200


@jwt_required()
def get_admin_by_id(id):
    """
    Get admin by id
    Call this route to get admin by id (only for super admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - admin_management
    parameters:
        - name: id
          in: path
          type: integer
          required: true
    responses:
        200:
            description: Admin
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    username:
                        type: string
                    role:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        403:
            description: Permission denied
        404:
            description: Admin not found
    """
    # check if current user is supper admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "super_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 403
    admin_id = id
    if not admin_id:
        return flask.jsonify({"msg": "Missing admin_id parameter"}), 400
    admin = Admin.query.filter_by(id=admin_id).first()
    if not admin:
        return flask.jsonify({"msg": "Admin not found"}), 404
    return flask.jsonify(admin.serialize()), 200


@jwt_required()
def delete_admin(id):
    """
    Delete admin
    Call this route to delete admin (only for super admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - admin_management
    parameters:
        - name: id
          in: path
          type: integer
          required: true
    responses:
        200:
            description: Admin deleted
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        403:
            description: Permission denied
        404:
            description: Admin not found
    """
    # check if current user is supper admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "super_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 403

    admin_id = id

    if not admin_id:
        return flask.jsonify({"msg": "Missing admin_id parameter"}), 400

    admin = Admin.query.filter_by(id=admin_id).first()

    # check if admin with this id exists
    if not admin:
        return flask.jsonify({"msg": "Admin with this id does not exists"}), 404

    db.session.delete(admin)
    db.session.commit()
    return flask.jsonify({"msg": "Admin deleted"}), 200


@jwt_required()
def change_admin_type():
    """
    Change admin type
    Call this route to change admin type (only for super admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - admin_management
    parameters:
    parameters:
        - name: body
          in: body
          schema:
                type: object
                properties:
                    id:
                        type: integer
                    role:
                        type: string
    responses:
        200:
            description: Admin type changed
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        403:
            description: Permission denied
        404:
            description: Admin not found
    """
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "super_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 403

    admin_id = flask.request.json.get('admin_id', None)
    admin_type = flask.request.json.get('admin_type', None)
    if not admin_id:
        return flask.jsonify({"msg": "Missing admin_id parameter"}), 400
    if not admin_type:
        return flask.jsonify({"msg": "Missing admin_type parameter"}), 400

    if admin_type not in ["admin", "super_admin"]:
        return flask.jsonify({"msg": "Admin type must be super_admin or admin"}), 400

    admin = Admin.query.filter_by(id=admin_id).first()
    if not admin:
        return flask.jsonify({"msg": "Admin with this id does not exists"}), 404
    admin.admin_type = admin_type
    db.session.commit()
    return flask.jsonify({"msg": "Admin type changed"}), 200


@jwt_required()
def modify_admin():
    """
    Modify admin
    Call this route to modify admin (only for super admins)
    ---
    security:
    - bearerAuth: []
    tags:
        - admin_management
    parameters:
    parameters:
        - name: body
          in: body
          schema:
                type: object
                properties:
                    id:
                        type: integer
                    username:
                        type: string
                    password:
                        type: string
    responses:
        200:
            description: Admin modified
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        403:
            description: Permission denied
        404:
            description: Admin not found
    """
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(username=current_user).first()
    if admin.admin_type != "super_admin":
        return flask.jsonify({"msg": "You are not supper admin("}), 403

    admin_id = flask.request.json.get('admin_id', None)
    username = flask.request.json.get('username', None)
    password = flask.request.json.get('password', None)

    if not admin_id:
        return flask.jsonify({"msg": "Missing admin_id parameter"}), 400

    admin = Admin.query.filter_by(id=admin_id).first()
    if not admin:
        return flask.jsonify({"msg": "Admin with this id does not exists"}), 404
    if username:
        admin.username = username
    if password:
        admin.password = password
    db.session.commit()
    return flask.jsonify({"msg": "Admin modified"}), 200


@jwt_required()
def modify_visit_request():
    """
    Modify visit request
    Call this route to modify visit request
    ---
    security:
    - bearerAuth: []
    tags:
        - visit_request
    parameters:
        - name: body
          in: body
          schema:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                    surname:
                        type: string
                    phone:
                        type: string
                    email:
                        type: string
                    visit_date:
                        type: string
                    visit_time:
                        type: string
                    visit_type:
                        type: string
                    visit_reason:
                        type: string
                    visit_status:
                        type: string
                    base64_image:
                        type: string
    responses:
        200:
            description: Visit request modified
            schema:
                type: object
                properties:
                    msg:
                        type: string
        400:
            description: Bad request (missing parameters)
        401:
            description: Login failed
        403:
            description: Permission denied
        404:
            description: Visit request not found
    """
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400


    visit_request_id = flask.request.json.get('id', None)
    name = flask.request.json.get('name', None)
    surname = flask.request.json.get('surname', None)
    phone = flask.request.json.get('phone', None)
    email = flask.request.json.get('email', None)
    visit_date = flask.request.json.get('visit_date', None)
    visit_time = flask.request.json.get('visit_time', None)
    visit_type = flask.request.json.get('visit_type', None)
    visit_reason = flask.request.json.get('visit_reason', None)
    visit_status = flask.request.json.get('visit_status', None)

    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if not visit_request:
        return flask.jsonify({"msg": "Visit request with this id does not exists"}), 404

    if name:
        visit_request.name = name
    if surname:
        visit_request.surname = surname
    if phone:
        visit_request.phone = phone
    if email:
        visit_request.email = email
    if visit_date:
        visit_request.visit_date = visit_date
    if visit_time:
        visit_request.visit_time = visit_time
    if visit_type:
        visit_request.visit_type = visit_type
    if visit_reason:
        visit_request.visit_reason = visit_reason
    if visit_status:
        visit_request.visit_status = visit_status

    image = flask.request.json.get('base64_image', None)
    if image:
        image_from_base64 = base64.b64decode(image)
        name = str(ImageCounter.query.first().counter) + '.jpg'
        ImageCounter.query.first().counter += 1
        db.session.commit()
        with open('images/profile_pic/' + name, "wb") as f:
            f.write(image_from_base64)
        visit_request.image = name
        db.session.commit()


    db.session.commit()
    return flask.jsonify({"msg": "Visit request modified"}), 200


def init_routes(app):
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/refresh', 'refresh', refresh, methods=['POST'])
    app.add_url_rule('/who_am_i', 'who_i_am', who_i_am, methods=['GET'])
    app.add_url_rule('/logout', 'logout', modify_token, methods=['DELETE'])
    app.add_url_rule('/add_request', 'add_visit_request', add_visit_request, methods=['POST'])
    app.add_url_rule('/get_requests', 'get_visit_requests', get_visit_requests, methods=['GET'])
    app.add_url_rule('/add_picture', 'add_picture', add_picture, methods=['POST'])
    app.add_url_rule('/get_picture_by_id/<id>', 'get_picture_by_id', get_picture_by_id, methods=['GET'])
    app.add_url_rule('/get_picture_by_path/<path>', 'get_picture_by_patch', get_picture_by_patch, methods=['GET'])
    app.add_url_rule('/get_not_approved_requests', 'get_not_approved_visit_requests', get_not_approved_visit_requests, methods=['GET'])
    app.add_url_rule('/get_approved_requests', 'get_approved_visit_request', get_approved_visit_request, methods=['GET'])
    app.add_url_rule('/get_request/<id>', 'get_visit_requests_by_id', get_visit_requests_by_id, methods=['GET'])
    app.add_url_rule('/approve_request', 'approve_visit_request', approve_visit_request, methods=['POST'])
    app.add_url_rule('/reject_request', 'reject_visit_request', reject_visit_request, methods=['POST'])
    app.add_url_rule('/delete_request', 'delete_visit_request', delete_visit_request, methods=['POST'])
    app.add_url_rule('/add_admin', 'add_admin', add_admin, methods=['POST'])
    app.add_url_rule('/get_admins', 'get_admins', get_admins, methods=['GET'])
    app.add_url_rule('/get_admin/<id>', 'get_admin_by_id', get_admin_by_id, methods=['GET'])
    app.add_url_rule('/delete_admin/<id>', 'delete_admin', delete_admin, methods=['DELETE'])
    app.add_url_rule('/change_admin_type', 'change_admin_type', change_admin_type, methods=['POST'])
    app.add_url_rule('/modify_admin', 'modify_admin', modify_admin, methods=['POST'])
    app.add_url_rule('/modify_request', 'modify_visit_request', modify_visit_request, methods=['POST'])
