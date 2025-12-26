from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from ..models.room import Room
from ..models.feature import Feature
from ..extensions import db

bp = Blueprint("rooms", __name__, url_prefix="/rooms")

@bp.route("", methods=["GET"])
def list_rooms():
    query = Room.query

    # Filters
    building_id = request.args.get("building_id", type=int)
    floor = request.args.get("floor", type=int)
    feature_codes = request.args.getlist("feature_codes")
    timestamp = request.args.get("timestamp")

    if building_id is not None:
        query = query.filter(Room.building_id == building_id)

    if floor is not None:
        query = query.filter(Room.floor == floor)

    if feature_codes:
        query = query.join(Room.features).filter(
            Feature.code.in_(feature_codes)
        )

    # Timestamp logic intentionally deferred (depends on Classes model)

    rooms = query.distinct().all()
    return jsonify([r.to_dict() for r in rooms])


@bp.route("/<int:room_id>", methods=["GET"])
def get_room(room_id):
    room = Room.query.get_or_404(room_id)
    return jsonify(room.to_dict())


@bp.route("", methods=["POST"])
def create_room():
    data = request.get_json()

    room = Room(
        number=data["number"],
        name=data.get("name"),
        building_id=data["building_id"],
        floor=data["floor"],
        capacity=data.get("capacity"),
        is_open=data.get("is_open", True),
        type_id=data.get("type_id"),
    )

    if "feature_ids" in data:
        room.features = Feature.query.filter(
            Feature.id.in_(data["feature_ids"])
        ).all()

    db.session.add(room)
    db.session.commit()

    return jsonify(room.to_dict()), 201


@bp.route("/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    data = request.get_json()

    for field in [
        "number", "name", "floor", "capacity", "is_open", "type_id"
    ]:
        if field in data:
            setattr(room, field, data[field])

    if "feature_ids" in data:
        room.features = Feature.query.filter(
            Feature.id.in_(data["feature_ids"])
        ).all()

    db.session.commit()
    return jsonify(room.to_dict())


@bp.route("/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return "", 204