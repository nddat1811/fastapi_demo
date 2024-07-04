from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Table
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
#     role = relationship("DbRole", secondary="user_role_association")


# class DbRole(Base):
#     __tablename__ = 'roles'
#     id = Column(Integer, primary_key = True)
#     name = Column(String)
#     created_at = Column(DateTime, default=func.current_timestamp()) 
#     updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
#     deleted_at = Column(DateTime, default=None) 
#     permissions = relationship("DbPermission", secondary="role_permission_association")
#     users = relationship("DbUser", secondary="user_role_association")

# class DbPermission(Base):
#     __tablename__ = 'permissions'
#     id = Column(Integer, primary_key = True)
#     name = Column(String)
#     created_at = Column(DateTime, default=func.current_timestamp()) 
#     updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
#     deleted_at = Column(DateTime, default=None) 

#     permissions = relationship("DbRole", secondary="role_permission_association")


# role_permission_association = Table(
#     'role_permission_association',
#     Base.metadata,
#     Column('role_id', Integer, ForeignKey('roles.id')),
#     Column('permission_id', Integer, ForeignKey('permissions.id'))
# )

# user_role_association = Table(
#     'user_role_association',
#     Base.metadata,
#     Column('role_id', Integer, ForeignKey('roles.id')),
#     Column('user_id', Integer, ForeignKey('users.id'))
# )