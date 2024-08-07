
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import db_user
from app.db.database import get_db
from app.schemas.authentication import RefreshTokenRequest, RegistrationRequest
from app.schemas.user import UserDisplay
from pydantic import BaseModel, EmailStr

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/register', status_code= status.HTTP_201_CREATED)
async def register(registration_request : RegistrationRequest, db : Session = Depends(get_db)):
    return await db_user.create_new_user(registration_request, db)

@router.post('/login2')
async def login(loginRequest : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    return await db_user.login(loginRequest, db)

class loginRequest(BaseModel):
    username: str
    password: str
@router.post('/login')
async def login(loginRequest: loginRequest, db : Session = Depends(get_db)):
    return await db_user.login(loginRequest, db)

@router.post('/refresh-token')
async def refresh_token(refresh_token_request : RefreshTokenRequest, db : Session = Depends(get_db)):
    return await db_user.refresh_token(refresh_token_request.token, db)