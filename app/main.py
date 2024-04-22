from fastapi import FastAPI, HTTPException, status, Response, Request
# from db import database
# from routers import user
from app.db.database import engine
from app import models
from app.routers import user, authentication

app = FastAPI()
# app.include_router(dependencies.router)
# app.include_router(email.router)

app.include_router(user.router)
app.include_router(authentication.router)

@app.get('/')
def index():
    return {"message": "Hello World"}


models.Base.metadata.create_all(engine)
