from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Table
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.sql import func


class SysFunction(Base):
    __tablename__ = 'SYS_FUNCTION'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    path = Column(String(255))
    description = Column(String(255))
    parent_id = Column(Integer, ForeignKey('SYS_FUNCTION.id'))
    type = Column(String(50))
    status = Column(Integer)
    icon_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(Integer)
    updated_by = Column(Integer)