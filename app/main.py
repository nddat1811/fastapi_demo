from app.middleware.log import LoggingMiddleware
# from db import database
from app.auth import authentication

from app.db.db_function import is_authentication
from app.models.user import SysUser
from app.routers import user
from app.db.database import engine, get_db
from app import models
from app.routers import user

from fastapi import APIRouter, Depends, HTTPException, Request, status, FastAPI

app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)


@app.get('/hiu')
def index():
    return {"message": "Hello World"}

# Add the middleware to the app
app.add_middleware(LoggingMiddleware)
models.Base.metadata.create_all(engine)
