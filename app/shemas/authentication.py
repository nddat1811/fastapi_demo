from pydantic import BaseModel, EmailStr
from .user import UserBase

from datetime import date

class RegistrationRequest(UserBase): 
    username : str
    password : str
    email : EmailStr
    dob : date

class AuthResponse(BaseModel):
    access_token : str
    request_token : str
    token_type : str

class RefreshTokenRequest(BaseModel): 
    token : str