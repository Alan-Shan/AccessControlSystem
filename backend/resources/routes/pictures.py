import base64
import os

import flask
from flask_jwt_extended import jwt_required

from database.db import db
from database.model.visitrequest import VisitRequest
from database.model.image_counter import ImageCounter


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
