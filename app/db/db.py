from typing import AsyncIterable
from dishka import Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.db.config import db_link


DATABASE_URL = db_link


engine = create_async_engine(url=DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db() -> AsyncIterable[AsyncSession]:
    async with async_session() as session:
        yield session

dbProvider = Provider(scope=Scope.REQUEST)
dbProvider.provide(get_db)
