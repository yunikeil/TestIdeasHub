from pydantic import Field, BaseModel


class SubjectCreate(BaseModel):
    name: str = "Математика"


class TeacherCreate(BaseModel):
    name: str = "Виталий Сергеевич"


class RoomCreate(BaseModel):
    capacity: int = Field(default=30, le=100)


class ScheduleCreate(BaseModel):
    subject_id: int
    teacher_id: int
    room_id: int
    day: int = Field(gt=0, le=12)
    time_slot: int = Field(gt=0, le=6)

