from app.db.database import Base
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class DbWaterBill(Base):
    __tablename__ = "water_bills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    prev_volume = Column(Integer)
    cur_volume = Column(Integer)
    total_volume = Column(Integer)
    price = Column(Integer)
    total_volume_price = Column(Integer)
    due_date = Column(DateTime)
    payment_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, default=None, server_default=func.now(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    user = relationship("DbUser", back_populates="bills")