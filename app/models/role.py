from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Table
from app.db.database import Base
from sqlalchemy.sql import func



class SysRole(Base):
    __tablename__ = 'SYS_ROLE'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    status = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(Integer)
    updated_by = Column(Integer)


class SysRoleFunction(Base):
    __tablename__ = 'SYS_ROLE_FUNCTION'
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('SYS_ROLE.id'))
    function_id = Column(Integer, ForeignKey('SYS_FUNCTION.id'))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(Integer)