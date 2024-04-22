from gc import disable
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import db_user
from app.db.database import get_db
from app.schemas.authentication import RefreshTokenRequest

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)
@router.post('/login')
async def login(loginRequest : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    return db_user.login(loginRequest, db)

@router.post('/refresh-token')
async def refresh_token(refresh_token_request : RefreshTokenRequest, db : Session = Depends(get_db)):
    return db_user.refresh_token(refresh_token_request.token, db)