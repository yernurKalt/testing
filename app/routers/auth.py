from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
from app.deps.hashed_password import oauth2_scheme
from app.models.user import User
from app.repositories.user import UserRepo
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.services.authenticate import authenticate_user, create_access_token, get_current_user
from app.services.user import UserService


router = APIRouter(prefix = "/token", tags=["token"])



@router.post("", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_db)],
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token({"sub": user.username}, expire_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

@router.get("")
async def get(user: Annotated[User, Depends(get_current_user)]):
    return UserOut.model_validate(user).model_dump()

@router.post("/register")
async def create_user(session: Annotated[AsyncSession, Depends(get_db)], user: UserCreate) -> UserOut:
    userService = UserService()
    
    return UserOut.model_validate(await userService.create_user(session, user)).model_dump()