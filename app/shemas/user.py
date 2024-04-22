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