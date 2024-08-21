from app.middleware.log import LoggingMiddleware
# from db import database
from app.auth import authentication


from app.routers import user
from app.db.database import engine, get_db
from app import models
from app.routers import user

from fastapi import FastAPI

app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)


@app.get('/hiu')
def index():
    return {"message": "Hello World"}

# Add the middleware to the app
app.add_middleware(LoggingMiddleware)
models.Base.metadata.create_all(engine)
