from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username : str
    email : EmailStr


class UserDisplay(UserBase):
    id : int
    message : str

class UserResetPasswordRequest(BaseModel):
    new_pass: str
    conf_pass: str
    user_id: int

class ResetPasswordResponse(BaseModel):
    id: int
    username: str
    email: str

class UpdateUserRequest(BaseModel):
    dob : date


class ForgotPasswordRequest(BaseModel):
    email: str

class CheckCodePasswordRequest(BaseModel):
    code: str