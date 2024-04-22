
from datetime import date
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username : str
    email : EmailStr
    dob : date

class RegistrationRequest(UserBase): 
    username : str
    password : str
    email : EmailStr
    dob : date

class UserResetPassword(BaseModel):
    new_pass: str
    conf_pass: str
    user_id: int

class ResetPasswordResponse(BaseModel):
    id: int
    username: str
    email: str
    dob: date