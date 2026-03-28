from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepo
from app.schemas.user import UserCreate
from app.deps.hashed_password import get_password_hashed


class UserService:
    def __init__(self):
        self.userRepo = UserRepo()

    async def get_user(self, session: AsyncSession, username: str) -> User:
        user = await self.userRepo.get_user_by_username(session, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user

    async def create_user(self, session: AsyncSession, user: UserCreate) -> User:
        if await self.userRepo.get_user_by_email(session, user.email) or await self.userRepo.get_user_by_username(session, user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with such email or username already exists",
                headers={"WWW-Authenticate": "Bearer"},
            )
        password = get_password_hashed(user.password)
        newUser = User(
            username=user.username, 
            hashed_password=password,
            email=user.email
        )
        return await self.userRepo.add_user(session, user=newUser)

        
 