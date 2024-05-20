from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database import get_session
from app.services import subject_manager, teacher_manager, room_manager, schedule_manager


api_router = APIRouter()


@api_router.post("/subjects", tags=["subjects"])
async def create_new_subject(
    subject: schemas.SubjectCreate,
    db_session: AsyncSession = Depends(get_session),
):
    subject = await subject_manager.create(db_session, subject)
    return subject


@api_router.post("/subjects/newteacher", tags=["subjects"])
async def add_teacher_subject(
    subject_id: int,
    teacher_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    teacher_subject = await subject_manager.add_teacher(db_session, subject_id, teacher_id)
    if not teacher_subject:
        raise HTTPException(404)
    
    return teacher_subject


@api_router.delete("/subjects", tags=["subjects"])
async def hide_subject(
    subject_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    subject = await subject_manager.hide(db_session, subject_id)
    if not subject:
        raise HTTPException(404)
    
    return subject


@api_router.post("/teachers", tags=["teachers"])
async def create_new_teacher(
    teacher: schemas.TeacherCreate,
    db_session: AsyncSession = Depends(get_session),
):
    teacher = await teacher_manager.create(db_session, teacher)
    return teacher


@api_router.delete("/teachers", tags=["teachers"])
async def hide_teacher(
    teacher_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    teacher = await teacher_manager.hide(db_session, teacher_id)
    if not teacher:
        raise HTTPException(404)
    
    return teacher


@api_router.post("/rooms", tags=["rooms"])
async def create_new_room(
    room: schemas.RoomCreate,
    db_session: AsyncSession = Depends(get_session),
):
    room = await room_manager.create(db_session, room)
    return room


@api_router.delete("/rooms", tags=["rooms"])
async def delete_room(
    room_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    room = await room_manager.delete(db_session, room_id)
    if not room:
        raise HTTPException(404)
    
    return room


@api_router.post("/schedules", tags=["schedules"])
async def create_new_schedule(
    schedule: schemas.ScheduleCreate,
    db_session: AsyncSession = Depends(get_session),
):
    schedule = await schedule_manager.create(db_session, schedule)
    return schedule


@api_router.delete("/schedules", tags=["schedules"])
async def delete_schedule(
    schedule_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    schedule = await schedule_manager.delete(db_session, schedule_id)
    if not schedule:
        raise HTTPException(404)
    
    return schedule


@api_router.get("/schedules", tags=["schedules"])
async def get_all_schedules(
    days: list[int] = Query(), offset: int = 0, limit: int = 50,
    db_session: AsyncSession = Depends(get_session),
):
    schedules = await schedule_manager.get_all_schedules(
        db_session, days, limit, offset
    )
    if not schedules:
        raise HTTPException(404)
    
    return schedules
