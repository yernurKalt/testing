from contextlib import asynccontextmanager
from typing import Annotated
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import DATABASE_URL, dbProvider, get_db
from app.repositories.user import UserRepoProvider
from app.routers.auth import router as auth_router
from app.routers.reserve import router as reserve_router
from app.routers.product import router as product_router
from app.routers.user import router as user_router
from app.schemas.user import UserCreate, UserOut
from app.services.user import UserService




def create_app():
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],       # Or ["*"] to allow all (not recommended for production)
    allow_credentials=True,      # Set to True if you need to support cookies/auth headers
    allow_methods=["*"],         # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allows all headers
)


    app.include_router(auth_router)
    app.include_router(reserve_router)
    app.include_router(product_router)
    app.include_router(user_router)
    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()

app = create_app()
container = make_async_container(dbProvider, UserRepoProvider())
setup_dishka(container=container, app=app)