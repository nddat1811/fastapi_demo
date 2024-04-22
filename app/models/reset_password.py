from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class DbResetPassword(Base):
    __tablename__ = 'reset_password'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    code = Column(String)
    expiry = Column(DateTime)

    user = relationship("users", back_populates="reset_password")