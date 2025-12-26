# api/routes/buildings.py
from flask import Blueprint, request, jsonify
from ..models.building import Building
from ..extensions import db

bp = Blueprint("buildings", __name__, url_prefix="/buildings")


@bp.route("", methods=["GET"])
def list_buildings():
    return jsonify([b.to_dict() for b in Building.query.all()])


@bp.route("", methods=["POST"])
def create_building():
    data = request.get_json()
    building = Building(**data)
    db.session.add(building)
    db.session.commit()
    return jsonify(building.to_dict()), 201
