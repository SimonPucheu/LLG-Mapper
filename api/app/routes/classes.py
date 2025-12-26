from flask import Blueprint, request, jsonify
from ..models.class_ import Class
from ..extensions import db

bp = Blueprint("classes", __name__, url_prefix="/classes")


@bp.route("", methods=["GET"])
def list_classes():
    classes = Class.query.all()
    return jsonify([c.to_dict() for c in classes])


@bp.route("/<int:class_id>", methods=["GET"])
def get_class(class_id):
    c = Class.query.get_or_404(class_id)
    return jsonify(c.to_dict())


@bp.route("", methods=["POST"])
def create_class():
    data = request.get_json()
    c = Class(**data)
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@bp.route("/<int:class_id>", methods=["PUT"])
def update_class(class_id):
    c = Class.query.get_or_404(class_id)
    data = request.get_json()

    for key, value in data.items():
        setattr(c, key, value)

    db.session.commit()
    return jsonify(c.to_dict())


@bp.route("/<int:class_id>", methods=["DELETE"])
def delete_class(class_id):
    c = Class.query.get_or_404(class_id)
    db.session.delete(c)
    db.session.commit()
    return "", 204
