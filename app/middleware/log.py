


import json
import logging
import time
from app.constant.log import URL_PATH_NOT_WRITE_LOG
from app.db.db_log import LogModel, write_log_DB
from app.middleware.auth import check_authentication
from sqlalchemy.orm import Session
from app.db.database import get_db
from datetime import  datetime
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.csv import  write_log_csv
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class LoggingMiddleware(BaseHTTPMiddleware):
    def get_original_path(self, route) -> str:
        if route:
            return route.path
        return "ERROR"

    def combine_params(self, request):
        #get query params and path params
        path_params = request.path_params
        query_params = dict(request.query_params)
        return str({
            "path": path_params,
            "query": query_params
        })
    def is_not_write_log(self, request, request_body):
        if URL_PATH_NOT_WRITE_LOG.get(request.url.path, False) or request.method == 'OPTIONS' or "multipart/form-data" in request.headers.get("content-type", "") or self.is_base64(request_body):
            return True
        return False
    def print_log(self, request, request_body, original_path):
        logger.info(
            f"\n{request.method} request to {request.url} metadata\n"
            # f"\path: {request.url.path}\n"
            f"\tBody: {request_body}\n"
            f"\tPath Params: {request.path_params}\n"
            f"\tQuery Params: {request.query_params}\n"
            f"\tOriginal path: {original_path}\n")
    def is_base64(self, s:str):
        return b"base64" in s
    async def write_log(self,  db: Session, request: Request, request_body: str, original_path: str,   
                status_code:int, body_str: str, process_time: float, error_message=None):
        # Combine query params and path params
        combined_params = self.combine_params(request=request)
        #define model to write log files
        print("body: ", body_str)
        client_ip = await self.get_real_ip(request)
        log_entry = LogModel(
            action_datetime=datetime.now(),
            path_name=original_path,
            method=request.method,
            ip=client_ip,
            status_response=status_code,
            response=body_str if error_message is None else error_message,
            duration=round(process_time, 3),
            request_body=request_body,
            request_query= combined_params,
            description=None
        )
        
        #write log csv
        write_log_csv(log_entry)
        #write log database
        write_log_DB(log_entry, db)
    async def get_real_ip(self, request: Request) -> str:
        headers_to_check = [
            "X-Forwarded-For",
            "X-Real-IP"
        ]

        for header in headers_to_check:
            if header in request.headers:
                return request.headers[header].split(",")[0].strip()

        return request.client.host
    async def dispatch(self, request: Request, call_next):
        flag = True
        db: Session = next(get_db())
        start_time = time.time()
        request_body = await request.body()
        response = await call_next(request)
        process_time = time.time() - start_time
        try:
            original_path = self.get_original_path(request.scope.get('route'))
            # if base64, file, OPTIONS method, some urls --> not write log --> return response 
            if not await check_authentication(request=request, db=db, original_path=original_path):
                flag = False
                response = JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={"detail": "Bạn không có quyền sử dụng tính năng này"}
                    )
            if self.is_not_write_log(request=request, request_body=request_body):  
                return response
            
            # Remove password field if the path is /login
            if request.url.path == "/auth/login":
                try:
                    request_body_json = json.loads(request_body)
                    
                    request_body_json.pop("password", None)
                    request_body = json.dumps(request_body_json)
                except json.JSONDecodeError:
                    # response.status_code = 500
                    flag = False
                    response = JSONResponse(
                        status_code=400,
                        content={"detail": "Invalid JSON format"}
                    )
            body_str = str("")
            if flag:
                body_iterator = response.body_iterator
                body = b"".join([section async for section in body_iterator])
                body_str = body.decode()
                response = Response(content=body_str, status_code=response.status_code, headers=dict(response.headers))
            else:
                body_str = str(response.body.decode())
            #print log to screen
            # self.print_log(request=request, request_body=request_body, original_path=original_path)
            # write log to csv and db
            await self.write_log(db=db, request=request, request_body=request_body, 
                        original_path=original_path, status_code=response.status_code,
                        body_str=body_str, process_time=process_time, error_message=None)
            return response
        except Exception as e:
            error_message = str(e)
            await self.write_log(db=db, request=request, request_body=request_body, 
                        original_path=original_path, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        body_str=str({"detail": "Internal Server Error"}), 
                        process_time=process_time, error_message=error_message)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )