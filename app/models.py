from time import time

import sqlalchemy
from sqlalchemy import text, event, Column, Integer, String, Boolean, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped


class Base(AsyncAttrs, DeclarativeBase):
    created_at = Column(Integer, default=lambda: int(time()), nullable=False)
    updated_at = Column(Integer, default=lambda: int(time()), onupdate=lambda: int(time()), nullable=False)

    def to_dict(self, base_dict: dict = {}):
        main_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return main_dict | base_dict


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    hidden = Column(Boolean, nullable=False, default=False)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    hidden = Column(Boolean, nullable=False,  default=False)


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer, nullable=False)


@event.listens_for(Room.__table__, "after_create")
def create_room_count_trigger(
    target: Room.__table__, connection: sqlalchemy.engine.base.Connection, **kw
):
    room_trigger = """
    CREATE TRIGGER 'room_count_check_trigger'
    BEFORE INSERT ON 'rooms'
    FOR EACH ROW
    BEGIN
        SELECT
            CASE
                WHEN (SELECT COUNT(*) FROM rooms) > 150 THEN
                    RAISE(ABORT, 'Max count must be <= 150')
            END;
    END;
    """
    connection.execute(text(room_trigger))


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    day = Column(Integer, CheckConstraint("day > 0 AND day <= 12", name="check_day"), nullable=False)
    # <= 12 т.к. 6 дней Нечётной + 6 дней Чётной недели, 6 тайм слотов - 6 пар
    time_slot = Column(Integer, CheckConstraint("time_slot > 0 AND time_slot <= 6", name="check_timeslot"), nullable=False)
    
    subject: Mapped["Subject"] = relationship(lazy="selectin")
    teacher: Mapped["Teacher"] = relationship(lazy="selectin")
    room: Mapped["Room"] = relationship(lazy="selectin")
    
    __table_args__ = (
        UniqueConstraint('room_id', 'time_slot', name='_room_id_time_slot_uc'),
        UniqueConstraint('teacher_id', 'day', 'time_slot', name='_teacher_id_day_time_slot_uc'),
    )
    
    def to_dict(self):
        base_dict = {
            "subject": self.subject,
            "teacher": self.teacher,
            "room": self.room,
        }
        return super().to_dict(base_dict)


class TeacherSubject(Base):
    __tablename__ = 'teachers_subjects'
    teacher_id = Column(Integer, ForeignKey('teachers.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
