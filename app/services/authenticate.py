from datetime import datetime, timedelta, timezone
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import algorithm, secret_key
from app.db.db import get_db
from app.deps.hashed_password import oauth2_scheme, verify_password
from app.repositories.user import UserRepo, UserRepoProvider
from app.repositories.ioc import repos_container




async def authenticate_user(session: AsyncSession, username: str, password: str, userRepo: UserRepo):
    user = await userRepo.get_user_by_username(session, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: FromDishka[AsyncSession],
    userRepo: FromDishka[UserRepo]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        # Bad signature, expired token, malformed JWT, wrong algorithm, etc.
        raise credentials_exception
    user = await userRepo.get_user_by_username(session, username)
    if not user:
        raise credentials_exception
    return user