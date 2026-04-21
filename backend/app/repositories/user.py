from dishka import Provider, Scope, provide
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepo:
    def __init__(self):
        pass

    async def get_user_by_username(self, session: AsyncSession, username: str) -> User | None:
        result = await session.execute(select(User).where(User.username == username))
        return (result.scalar_one_or_none())
    
    async def get_user_by_email(self, session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return (result.scalar_one_or_none())

    async def get_all_users(self, session: AsyncSession) -> list[User]:
        result = await session.execute(select(User).order_by(User.id))
        return list(result.scalars().all())

    async def add_user(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        return user


class UserRepoProvider(Provider):
    provider = provide(UserRepo, scope=Scope.APP)
