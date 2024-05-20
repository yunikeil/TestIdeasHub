import logging
import contextlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.models import Base, Room, Teacher, Subject


DATABASE_URL = "sqlite+aiosqlite:///./school_schedule.db?_fk=1"


logger = logging.getLogger("uvicorn")
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_models(*, drop_all=False):
    async with engine.begin() as conn:
        if drop_all:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Init models finished.")


async def preload_db(db_session: AsyncSession):
    exists = (await db_session.execute(select(Room))).scalars().all()
    if exists:
        logger.info("Init base_db finished with exists.")
        return
    
    rooms = [Room(capacity=30), Room(capacity=25), Room(capacity=20)]
    teachers = [Teacher(name="Мария Филатова")]
    subjects = [Subject(name="Физика")]
    db_session.add_all([*rooms, *teachers, *subjects])
    
    await db_session.commit()
    logger.info("Init base_db finished.")


async def get_session():
    async with async_session() as session:
        yield session


@contextlib.asynccontextmanager
async def context_get_session():
    async with async_session() as session:
        yield session
