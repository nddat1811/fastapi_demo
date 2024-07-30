from fastapi import FastAPI, HTTPException, status, Response, Request
# from db import database
from app.auth import authentication
from app.db.db_log import LogModel, log_FILE
from app.routers import user
from app.db.database import engine, get_db
from app import models
from app.routers import user
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import date, datetime
app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_body = await request.body()
        
        # Log request details
        logger.warning(f"Request: {request.method} {request.url.path} from {request.client.host}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Log response details
        logger.warning(
            f"Response: {response.status_code} "
            f"for {request.method} {request.url.path} "
            f"from {request.client.host} "
            f"in {process_time:.2f} seconds"
        )
        #response
        body_iterator = response.body_iterator
        body = b"".join([section async for section in body_iterator])
        body_str = body.decode()
        print("HMM")
        response = Response(content=body_str, status_code=response.status_code, headers=dict(response.headers))
        response.headers["Content-Length"] = str(len(body_str))
        
        
        print("res:", request_body)

        logger.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )

        req = LogModel(
            action_datetime = datetime.now(),
            path_name=request.url.path,
            method=request.method,
            ip=request.client.host,
            status_response= response.status_code,
            response=body_str,
            duration=process_time,
            request="t",
        )
        db: Session = next(get_db())
        log_FILE(req, db)
        return response

@app.get('/hiu')
def index():
    return {"message": "Hello World"}

# Add the middleware to the app
app.add_middleware(LoggingMiddleware)
models.Base.metadata.create_all(engine)
