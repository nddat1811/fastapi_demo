from sqlalchemy import Column, Integer, String, DateTime, Float,Text
from sqlalchemy.orm import relationship
from app.db.database import Base



class SysLog(Base):
    __tablename__ = 'SYS_LOG'
    id = Column(Integer, primary_key=True, index=True)
    action_datetime = Column(DateTime)
    path_name = Column(String(255))
    method = Column(String(50))
    ip = Column(String(50))
    status_response = Column(Integer)
    response = Column(Text)
    description = Column(String(255))
    request_body = Column(Text)
    request_query = Column(Text)
    duration = Column(Float)
    