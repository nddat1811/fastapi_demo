from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
from ..db.database import get_db
from jose import JWTError, jwt
from app.db import db_user
from ..models.user import DbUser

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = 'fba012a2a0c9c3d884fdf15843f2aa438bac1b5e8527875ecd7187e3ce494158'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESHER_TOKEN_EXPIRE_MINUTES = 3000

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalidate token",
        headers={'WWW-Authorization' : 'Bearer'}
)

#Get current user
async def get_current_user(token : str = Depends(oauth2_bearer), db : Session = Depends(get_db)) -> DbUser:
    username = extract_claim(claim_type = 'sub', token=token)
    user = await db_user.get_user_by_username(username, db)
    
    if user is None: 
        raise credentials_exception
    return user

#Create access token
def create_token(claims: dict, expire_delta_time : Optional[timedelta] = None):

    if expire_delta_time:
        expire_time = datetime.now(timezone.utc)+ expire_delta_time
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode = claims.copy()
    to_encode.update({'exp' : expire_time})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return jwt_token

def extract_claim(claim_type : str, token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        claim : str = payload.get(claim_type)
        if claim is None:
            raise credentials_exception
        
    except JWTError:
        print('decode error')
        raise credentials_exception
    return claim

class RoleChecker:
  def __init__(self, allowed_roles):
    self.allowed_roles = allowed_roles

  def __call__(self, user: DbUser = Depends(get_current_user)):
    if user.role in self.allowed_roles:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="You don't have enough permissions"
        )
