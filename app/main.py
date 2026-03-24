from fastapi import FastAPI
from app.db.db import DATABASE_URL
from app.routers.auth import router as auth_router


app = FastAPI()

app.include_router(auth_router)