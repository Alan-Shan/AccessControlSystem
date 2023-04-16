import base64
import os

import flask
from flask_jwt_extended import jwt_required

from database.db import db
from database.model.visitrequest import VisitRequest
from database.model.image_counter import ImageCounter

import re

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
        extension = image.split(';')[0].split('/')[1]
        image = image.split(',')[1]
        image_from_base64 = base64.b64decode(image)
        counter = ImageCounter.query.first()
        name = str(counter.counter) + "." + extension
        counter.counter += 1
        db.session.commit()
        # create folder if not exists
        if not os.path.exists('images/profile_pic'):
            os.makedirs('images/profile_pic')
        with open('images/profile_pic/' + name, "wb") as f:
            f.write(image_from_base64)
        visit_request.image_path = name
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

    # # check if visit request with this email already exists
    # if VisitRequest.query.filter_by(email=visit_request.email).first() is not None:
    #     return flask.jsonify({"msg": "Visit request with this email already exists"}), 400
    # # check if visit request with this phone already exists
    # if VisitRequest.query.filter_by(phone=visit_request.phone).first() is not None:
    #     return flask.jsonify({"msg": "Visit request with this phone already exists"}), 400
    # # check if visit request with this document number already exists
    # if VisitRequest.query.filter_by(document_number=visit_request.document_number).first() is not None:
    #     return flask.jsonify({"msg": "Visit request with this document number already exists"}), 400

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
def approve_visit_request(id):
    """
    Approve visit request
    Call this route to approve visit request (only for admins)
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

    visit_request_id = id
    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if not visit_request:
        return flask.jsonify({"msg": "Visit request not found"}), 400
    visit_request.status = 'approved'
    db.session.commit()
    return flask.jsonify({"msg": "Visit request approved"}), 200


@jwt_required()
def reject_visit_request(id):
    """
    Reject visit request
    Call this route to reject visit request (only for admins)
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
    visit_request_id = id

    if not visit_request_id:
        return flask.jsonify({"msg": "Missing visit_request_id parameter"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if not visit_request:
        return flask.jsonify({"msg": "Visit request not found"}), 400
    visit_request.status = "rejected"
    db.session.commit()
    return flask.jsonify({"msg": "Visit request rejected"}), 200

@jwt_required()
def delete_visit_request(id):
    """
    Delete visit request
    Call this route to delete visit request (only for admins)
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
    visit_request_id = id
    if visit_request_id is None:
        return flask.jsonify({"msg": "Visit request id is not specified"}), 400

    visit_request = VisitRequest.query.filter_by(id=visit_request_id).first()
    if visit_request is None:
        return flask.jsonify({"msg": "Visit request not found"}), 400

    db.session.delete(visit_request)
    db.session.commit()
    return flask.jsonify({"msg": "Visit request deleted"}), 200

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
        extension = image.split(';')[0].split('/')[1]
        image = image.split(',')[1]
        image_from_base64 = base64.b64decode(image)
        counter = ImageCounter.query.first()
        name = str(counter.counter) + "." + extension
        counter.counter += 1
        db.session.commit()
        # create folder if not exists
        if not os.path.exists('images/profile_pic'):
            os.makedirs('images/profile_pic')
        with open('images/profile_pic/' + name, "wb") as f:
            f.write(image_from_base64)
        visit_request.image_path = name
        db.session.commit()

    db.session.commit()
    return flask.jsonify({"msg": "Visit request modified"}), 200