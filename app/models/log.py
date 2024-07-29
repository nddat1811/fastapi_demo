from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Table
from sqlalchemy.orm import relationship
from app.db.database import Base



class SysLog(Base):
    __tablename__ = 'SYS_LOG'
    id = Column(Integer, primary_key=True, index=True)
    action_datetime = Column(DateTime)
    path_name = Column(String(255))
    method = Column(String(50))
    ip = Column(String(50))
    status_response = Column(String(50))
    response = Column(String(255))
    description = Column(String(255))
    request = Column(String(255))
    duration = Column(float)