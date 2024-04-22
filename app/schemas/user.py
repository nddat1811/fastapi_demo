
from datetime import date
from pydantic import BaseModel, EmailStr
from app.utils.constants import Role

class UserBase(BaseModel):
    username : str
    email : EmailStr
    dob : date

class UserDisplay(UserBase):
    id : int
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
    id : int
    role : Role
    dob : date

class UpdateRoleRequest(BaseModel):
    id : int
    role : Role

class ForgotPasswordRequest(BaseModel):
    email: str

class CheckCodePasswordRequest(BaseModel):
    code: str