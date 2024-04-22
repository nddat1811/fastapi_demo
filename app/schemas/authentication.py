from pydantic import BaseModel, EmailStr
from ..schemas.user import UserBase

from datetime import date

class RegistrationRequest(UserBase): 
    password : str

class AuthResponse(BaseModel):
    access_token : str
    request_token : str
    token_type : str

class RefreshTokenRequest(BaseModel): 
    token : str
