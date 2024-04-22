from app.db.database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class DbWaterBill(Base):
    __tablename__ = "water_bills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    prev_volume = Column(Integer)
    now_volume = Column(Integer)
    total_volume = Column(Integer)
    price = Column(Integer)
    due_date = Column(DateTime)
    payment_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True, default=None, server_default=func.now(), onupdate=func.current_timestamp())

    user = relationship("DbUser", back_populates="bills")