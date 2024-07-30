from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.utils.constants import Role

class UserBase(BaseModel):
    username : str
    email : EmailStr


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

class UpdateUserRequest(BaseModel):
    role : Role
    dob : date

class UpdateRoleRequest(BaseModel):
    role : Role

class ForgotPasswordRequest(BaseModel):
    email: str

class CheckCodePasswordRequest(BaseModel):
    code: str