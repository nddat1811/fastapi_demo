from fastapi import FastAPI, HTTPException, status, Response, Request
# from db import database
from app.auth import authentication
from app.routers import user
from app.db.database import engine
from app import models
from app.routers import user, water_bill, crawl
import logging
import time

app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)

@app.get('/')
def index():
    return {"message": "Hello World"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request details
        logger.info(f"Request: {request.method} {request.url.path} from {request.client.host}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Log response details
        logger.info(
            f"Response: {response.status_code} "
            f"for {request.method} {request.url.path} "
            f"from {request.client.host} "
            f"in {process_time:.2f} seconds"
        )
        
        return response

# Add the middleware to the app
app.add_middleware(LoggingMiddleware)
models.Base.metadata.create_all(engine)
