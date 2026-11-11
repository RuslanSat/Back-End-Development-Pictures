from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture is None:
        return jsonify(Message=f"picture with id {id} not found"), 404
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json(silent=True)
    required = {"id", "pic_url", "event_country", "event_state", "event_city", "event_date"}
    if not isinstance(picture, dict) or not required.issubset(picture):
        return jsonify(Message="a complete JSON picture is required"), 400
    if type(picture["id"]) is not int:
        return jsonify(Message="picture id must be an integer"), 400
    if any(item["id"] == picture["id"] for item in data):
        return jsonify(Message=f"picture with id {picture['id']} already present"), 302
    data.append(dict(picture))
    response = jsonify(picture)
    response.status_code = 201
    response.headers["Location"] = url_for("get_picture_by_id", id=picture["id"])
    return response

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture is None:
        return jsonify(Message=f"picture with id {id} not found"), 404
    replacement = request.get_json(silent=True)
    if not isinstance(replacement, dict) or replacement.get("id", id) != id:
        return jsonify(Message="valid JSON and an unchanged picture id are required"), 400
    picture.update(replacement)
    picture["id"] = id
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture["id"] == id:
            del data[index]
            return "", 204
    return jsonify(Message=f"picture with id {id} not found"), 404
