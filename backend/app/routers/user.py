from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepo
from app.schemas.user import UserOut
from app.services.authenticate import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/all")
@inject
async def get_all_users(
    session: FromDishka[AsyncSession],
    userRepo: FromDishka[UserRepo],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[UserOut]:
    users = await userRepo.get_all_users(session)
    return [UserOut.model_validate(u) for u in users]