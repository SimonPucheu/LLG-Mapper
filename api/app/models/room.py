from ..extensions import db

class Room(db.Model):
    __tablename__ = "rooms"
    
    __table_args__ = (
        db.UniqueConstraint(
            "building_id",
            "number",
            name="uq_room_number_per_building"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50))
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer)
    is_open = db.Column(db.Boolean, default=True)
    type_id = db.Column(db.Integer, db.ForeignKey("room_types.id"), nullable=False, default=0)
    locationX = db.Column(db.Integer, nullable=False)
    locationY = db.Column(db.Integer, nullable=False)
    sizeX = db.Column(db.Integer, nullable=False)
    sizeY = db.Column(db.Integer, nullable=False)
    
    building = db.relationship("Building", back_populates="rooms")
    type = db.relationship("RoomType", back_populates="rooms")
    features = db.relationship("Feature", secondary="room_features", back_populates="rooms")
    classes = db.relationship("Class", back_populates="room")

    @property
    def display_name(self):
        if self.name:
            return self.name
        return f"{self.building.code}{self.number:03d}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.display_name,
            "number": self.number,
            "floor": self.floor,
            "capacity": self.capacity,
            "is_open": self.is_open,
            "location": [self.locationX, self.locationY],
            "size": [self.sizeX, self.sizeY],
            "building": self.building.to_dict() if self.building else None,
            "type": self.type.to_dict() if self.type else None,
            "features": [f.to_dict() for f in self.features] if self.features else []
        }