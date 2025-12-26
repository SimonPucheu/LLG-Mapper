from flask import Blueprint, jsonify

example_bp = Blueprint("example", __name__)

@example_bp.route("/example", methods=["GET"])
def get_example():
    return jsonify([
        {"data": "blob", "boolVariable": True},
        {"data": "row2", "boolVariable": False}
    ])
