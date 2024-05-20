from typing import Any 
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update, extract
from fastapi.exceptions import HTTPException

from app.models import Subject, Teacher, Room, Schedule, TeacherSubject
from app.schemas import SubjectCreate, TeacherCreate, RoomCreate, ScheduleCreate


class SubjectManager:
    def __init__(self) -> None:
        pass

    async def create(self, db_session: AsyncSession, subject: SubjectCreate):
        create_stmt = (
            insert(Subject)
            .values(subject.model_dump())
            .returning(Subject)
        )
        q = await db_session.execute(create_stmt)
        await db_session.commit()
        await db_session.refresh(subject_ := q.scalar_one_or_none())
        return subject_
    
    async def add_teacher(self, db_session: AsyncSession, subject_id: int, teacher_id: int):
        create_stmt = (
            insert(TeacherSubject)
            .values(teacher_id=teacher_id, subject_id=subject_id)
            .returning(TeacherSubject)
        )
        q = await db_session.execute(create_stmt)
        await db_session.commit()
        await db_session.refresh(teacher_subject_ := q.scalar_one_or_none())
        return teacher_subject_
    
    async def hide(self, db_session: AsyncSession, subject_id: int):
        hide_stmt = (
            update(Subject)
            .where(Subject.id == subject_id)
            .values(hidden=True)
            .returning(Subject)
        )
        q = await db_session.execute(hide_stmt)
        await db_session.commit()
        await db_session.refresh(subject_ := q.scalar_one_or_none())
        return subject_


class TeacherManager:
    def __init__(self) -> None:
        pass
    
    async def create(self, db_session: AsyncSession, teacher: TeacherCreate):
        create_stmt = (
            insert(Teacher)
            .values(teacher.model_dump())
            .returning(Teacher)
        )
        q = await db_session.execute(create_stmt)
        await db_session.commit()
        await db_session.refresh(teacher_ := q.scalar_one_or_none())
        return teacher_

    async def hide(self, db_session: AsyncSession, teacher_id: int):
        hide_stmt = (
            update(Teacher)
            .where(Teacher.id == teacher_id)
            .values(hidden=True)
            .returning(Teacher)
        )
        q = await db_session.execute(hide_stmt)
        await db_session.commit()
        await db_session.refresh(teacher_ := q.scalar_one_or_none())
        return teacher_


class RoomManager:
    def __init__(self) -> None:
        pass

    async def create(self, db_session: AsyncSession, room: RoomCreate):
        create_stmt = (
            insert(Room)
            .values(room.model_dump())
            .returning(Room)
        )
        q = await db_session.execute(create_stmt)
        await db_session.commit()
        await db_session.refresh(room_ := q.scalar_one_or_none())
        return room_

    async def delete(self, db_session: AsyncSession, room_id: int):
        delete_stmt = (
            delete(Room)
            .where(Room.id == room_id)
            .returning(Room)
        )
        q = await db_session.execute(delete_stmt)
        await db_session.commit()
        return q.scalar_one_or_none()


class SchdeuleManager:
    def __init__(self) -> None:
        pass

    async def create(self, db_session: AsyncSession, schedule: ScheduleCreate):
        create_stmt = (
            insert(Schedule)
            .values(schedule.model_dump())
            .returning(Schedule)
        )
        q = await db_session.execute(create_stmt)
        await db_session.commit()
        await db_session.refresh(schedule_ := q.scalar_one_or_none())
        return schedule_

    
    async def get_all_schedules(self, db_session: AsyncSession, days: list[int], limit: int, offset: int):
        get_all_stmt = (
            select(Schedule)
            .where(Schedule.day.in_(days))
            .limit(limit)
            .offset(offset)
        )
        rows = await db_session.execute(get_all_stmt)
        return rows.scalars().all()
    
    async def delete(self, db_session: AsyncSession, schedule_id: int):
        delete_stmt = (
            delete(Schedule)
            .where(Schedule.id == schedule_id)
            .returning(Schedule)
        )
        q = await db_session.execute(delete_stmt)
        await db_session.commit()
        return q.scalar_one_or_none()


subject_manager = SubjectManager()
teacher_manager = TeacherManager()
room_manager = RoomManager()
schedule_manager = SchdeuleManager()
