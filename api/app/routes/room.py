from flask import Blueprint, jsonify
from ..models.room import Room

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])
