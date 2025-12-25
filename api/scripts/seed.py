import json
from pathlib import Path

from app import create_app, db
from app.models import Building, Room, RoomType, Feature

app = create_app()

DATA_PATH = Path(__file__).parent / "data" / "rooms.json"

def get_or_create(model, defaults=None, **kwargs):
    """Helper: get or create an object by filter."""
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    params = dict(**kwargs)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    db.session.add(instance)
    db.session.commit()
    return instance

with app.app_context():
    # Load JSON
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    # Seed RoomTypes
    room_type_objs = {}
    for rt in data.get("room_types", []):
        obj = get_or_create(RoomType, code=rt["code"], defaults={"name": rt["name"]})
        room_type_objs[obj.code] = obj

    # Seed Features
    feature_objs = {}
    for f in data.get("features", []):
        obj = get_or_create(Feature, code=f["code"], defaults={"name": f["name"]})
        feature_objs[obj.code] = obj

    # Seed Buildings and Rooms
    for b in data.get("buildings", []):
        building = get_or_create(Building, code=b["code"], defaults={"name": b["name"]})

        for r in b.get("rooms", []):
            # Default room type = CLASS
            type_code = r.get("type", "CLASS")
            room_type = room_type_objs[type_code]

            room = Room.query.filter_by(building_id=building.id, number=r["number"]).first()
            if not room:
                room = Room(
                    number=r["number"],
                    floor=r["floor"],
                    capacity=r.get("capacity"),
                    name=r.get("name"),
                    building=building,
                    type=room_type
                )
                db.session.add(room)
                db.session.commit()

            # Assign features
            features = []
            for f_code in r.get("features", []):
                feature = feature_objs.get(f_code)
                if feature:
                    features.append(feature)
            room.features = features
            db.session.commit()

    print("Database seeded successfully.")
