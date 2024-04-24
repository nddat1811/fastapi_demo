from fastapi import FastAPI, HTTPException, status, Response, Request
# from db import database
from app.auth import authentication
from app.routers import user
from app.db.database import engine
from app import models
from app.routers import user, water_bill

app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(water_bill.router)

@app.get('/')
def index():
    return {"message": "Hello World"}


models.Base.metadata.create_all(engine)
