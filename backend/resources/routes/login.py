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