from fastapi import FastAPI
from app.db.db import DATABASE_URL


app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": DATABASE_URL}