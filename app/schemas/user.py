from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.utils.constants import Role

class UserBase(BaseModel):
    username : str
    email : EmailStr
    dob : date

class User2Base(BaseModel):
    username: str
    email: str
    code: Optional[str] = None
    expiry: datetime
    refresh_token: Optional[str] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None
    role: str
    id: int
    hashed_password: Optional[str] = None
    dob: datetime
    last_login: Optional[datetime] = None
    updated_at: datetime

class User3Base(BaseModel):
    message: str
    data: User2Base

class UserDisplay(UserBase):
    id : int
    message : str
    role : Role

class UserResetPasswordRequest(BaseModel):
    new_pass: str
    conf_pass: str
    user_id: int

class ResetPasswordResponse(BaseModel):
    id: int
    username: str
    email: str
    dob: date

class UpdateUserRequest(BaseModel):
    role : Role
    dob : date

class UpdateRoleRequest(BaseModel):
    role : Role

class ForgotPasswordRequest(BaseModel):
    email: str

class CheckCodePasswordRequest(BaseModel):
    code: str