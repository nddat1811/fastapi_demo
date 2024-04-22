from app.db.database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship



class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    expiry = Column(DateTime)
    # items = relationship("DbArticle", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password