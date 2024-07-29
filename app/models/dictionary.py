from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Table
from sqlalchemy.orm import relationship
from app.db.database import Base


class DataDictionary(Base):
    __tablename__ = 'DATA_DICTIONARY'
    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(255))
    column_name = Column(String(255))
    description = Column(String(255))
    value = Column(Integer)