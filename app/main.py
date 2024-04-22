from fastapi import FastAPI, HTTPException, status, Response, Request
# from db import database
# from routers import user
from app.db.database import Base, engine
from app import models

app = FastAPI()
# app.include_router(dependencies.router)
# app.include_router(email.router)

@app.get('/')
def index():
    return {"message": "Hello World"}


models.Base.metadata.create_all(engine)