from ..extensions import db

class RoomType(db.Model):
    __tablename__ = "room_types"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    rooms = db.relationship("Room", back_populates="room_type")

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
        }