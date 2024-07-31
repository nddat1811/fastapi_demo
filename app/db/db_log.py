from typing import Optional
from pydantic import BaseModel
from app.models.log import SysLog
from datetime import date, datetime
from sqlalchemy.orm import Session

class LogModel(BaseModel):
    action_datetime: datetime 
    path_name: str
    method: str
    ip:str
    status_response: int
    response: str
    request_body: Optional[str]
    request_query: Optional[str]
    description: Optional[str]
    duration: float
    
    
def write_log_DB(req: LogModel, db : Session):
    log = SysLog(
        action_datetime=req.action_datetime,
        path_name=req.path_name,
        method=req.method,
        ip=req.ip,
        status_response=req.status_response,
        response=req.response,
        request_body=req.request_body,
        request_query=req.request_query,
        description= req.description,
        duration=req.duration
    )

    db.add(log)
    db.commit()
    return "DONE LOG"