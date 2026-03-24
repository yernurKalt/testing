from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepo
from app.schemas.user import UserCreate
from app.deps.hashed_password import get_password_hashed


class UserService:
    def __init__(self):
        self.userRepo = UserRepo()

    async def get_user(self, session: AsyncSession, username: str) -> User:
        return await self.userRepo.get_user_by_username(session, username)

    async def create_user(self, session: AsyncSession, user: UserCreate) -> User:
        password = get_password_hashed(user.password)
        newUser = User(
            username=user.username,
            hashed_password=password,
            email=user.email
        )
        return await self.userRepo.add_user(session, user=newUser)

        
