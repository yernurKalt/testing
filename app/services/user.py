from dishka.integrations.fastapi import FromDishka, inject
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.ioc import repos_container
from app.repositories.user import UserRepo, UserRepoProvider
from app.schemas.user import UserCreate
from app.deps.hashed_password import get_password_hashed


class UserService:
    async def create_user(self, session: AsyncSession, user: UserCreate) -> User:
        userRepo = await repos_container.get(UserRepo)
        if await userRepo.get_user_by_email(session, user.email) or await userRepo.get_user_by_username(session, user.username):
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
        return await userRepo.add_user(session, user=newUser)

        
 