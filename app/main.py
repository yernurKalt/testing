from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import DATABASE_URL, get_db
from app.routers.auth import router as auth_router
from app.routers.reserve import router as reserve_router
from app.routers.product import router as product_router
from app.schemas.user import UserCreate, UserOut
from app.services.sched.main import lifespan
from app.services.user import UserService


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(reserve_router)
app.include_router(product_router)


