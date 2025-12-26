from ..extensions import db
from .enums import Frequency

class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)

    # Date range
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # NULL = one-off

    # Time (same every occurrence)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    # Recurrence
    recurrence = db.Column(
        db.Enum(Frequency, name="class_frequency"),
        nullable=False,
        default=Frequency.WEEKLY
    )

    # 0 = Monday, 6 = Sunday
    weekday = db.Column(db.Integer)

    room = db.relationship("Room", back_populates="classes")
    teacher = db.relationship("Teacher", back_populates="classes")
    group = db.relationship("Group", back_populates="classes")
    subject = db.relationship("Subject", back_populates="classes")

    def to_dict(self):
        return {
            "id": self.id,
            "room": self.room.to_dict() if self.room else None,
            "teacher": self.teacher.to_dict() if self.teacher else None,
            "group": self.group.to_dict() if self.group else None,
            "subject": self.subject.to_dict() if self.subject else None,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "recurrence": self.recurrence,
            "weekday": self.weekday
        }