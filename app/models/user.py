from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    role = Column(String, nullable = False) 
    username = Column(String, unique = True)
    hashed_password = Column(String)
    email = Column(String, unique=True)
    dob = Column(Date)
    code = Column(String)
    expiry = Column(DateTime)
    refresh_token = Column(String)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=func.current_timestamp()) 
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, default=None) 

    bills = relationship("DbWaterBill", back_populates="user", foreign_keys="DbWaterBill.user_id")
    created_bills = relationship("DbWaterBill", back_populates="creator", foreign_keys="DbWaterBill.created_by")