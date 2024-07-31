


import json
import logging
import time
from app.constant.log import URL_PATH_NOT_WRITE_LOG
from app.db.db_log import LogModel, write_log_DB
from app.middleware.auth import check_authentication
from sqlalchemy.orm import Session
from app.db.database import get_db
from datetime import  datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.csv import  write_log_csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class LoggingMiddleware(BaseHTTPMiddleware):
    def get_original_path(self, route) -> str:
        if route:
            return route.path
        return "ERROR"

    def combine_params(self, query_params, path_params):
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
    def is_base64(self, s):
        return b"base64" in s
    
    async def dispatch(self, request: Request, call_next):
        db: Session = next(get_db())
        start_time = time.time()
        request_body = await request.body()
        
        # Log request details
        # logger.warning(f"Request: {request.method} {request.url.path} from {request.client.host}")
        
        # if(is_not_authen(request.url.path)):
        #     try:
        #         token = request.headers.get('Authorization').split(" ")[1]
        #         current_user: SysUser = await get_current_user(token, db)
        #         user_info = f"User: {current_user.id}"
        #         print(request.url.path)    
        #         # t = is_authentication(current_user.id, request.url.path, db)
        #     except Exception as e:
        #         user_info = "User: Unauthenticated"
        #         logger.error(f"Authentication error: {str(e)}")
        # else:
        #     print('con lai in ra')
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        #log to screen
        original_path = self.get_original_path(request.scope.get('route'))

        # if base64, file, OPTIONS method, some urls --> not write log --> return response 
        if self.is_not_write_log(request=request, request_body=request_body):  
            return response
        #response
        print("auth: ", await check_authentication(request=request, db=db, original_path=original_path))
        body_iterator = response.body_iterator
        body = b"".join([section async for section in body_iterator])
        body_str = body.decode()
        response = Response(content=body_str, status_code=response.status_code, headers=dict(response.headers))


        # Remove password field if the path is /login
        # if request.url.path == "/auth/login":
        #     try:
        #         request_body_json = json.loads(request_body)
                
        #         request_body_json.pop("password", None)
        #         request_body = json.dumps(request_body_json)
        #     except json.JSONDecodeError:
        #         pass
        #get query params and path params
        path_params = request.path_params
        query_params = dict(request.query_params)

        # Combine query params and path params
        combined_params = self.combine_params(query_params=query_params, path_params=path_params)
        #print log to screen
        # self.print_log(request=request, request_body=request_body, original_path=original_path)
        #define model to write log files
        log_entry = LogModel(
            action_datetime = datetime.now(),
            path_name=original_path,
            method=request.method,
            ip=request.client.host,
            status_response= response.status_code,
            response=body_str,
            duration=process_time,
            request_body=request_body,
            request_query=combined_params,
        )
        #write log csv
        write_log_csv(log_entry)
        #write log database
        write_log_DB(log_entry, db)
        return response
        # original_path = request.scope['root_path'] + request.scope['route'].path
        # print(f"Original Path: {request.scope.get('route')}\n\n")