from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from jobify import Jobify
from app.services.sched.routers.reserve import router as reserve_router


jobify_app = Jobify()

jobify_app.include_router(reserve_router)

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    async with jobify_app:
        yield