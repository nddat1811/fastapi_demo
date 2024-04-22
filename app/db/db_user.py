from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.models.user import DbUser
from app.shemas.authentication import AuthResponse
from app.shemas.user import RegistrationRequest

from . import hash, oauth2


def create_new_user(registration_request : RegistrationRequest, db : Session):
    user = DbUser(
        username = registration_request.username,
        hashed_password = hash.Hash.bcrypt(registration_request.password),
        email = registration_request.email,
        dob = registration_request.dob,
        role = 'user'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login(request : OAuth2PasswordRequestForm, db: Session):
    user = get_user_by_username(request.username, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    if not hash.Hash.verify(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid user"
        )
    access_token = oauth2.create_token({'sub' : user.username})
    refresh_token = oauth2.create_token({'sub' : user.username}, timedelta(weeks=1))

    user.refresh_token = refresh_token
    db.commit()

    return AuthResponse(
        access_token = access_token,
        request_token = refresh_token,
        token_type = 'bearer'
    )

def refresh_token(token : str, db: Session):
    username = oauth2.extract_claim(claim_type = 'sub', token=token)

    user = get_user_by_username(username, db)

    if user is None: 
        raise oauth2.credentials_exception
    
    if token != user.refresh_token: 
        raise oauth2.credentials_exception
    
    access_token = oauth2.create_token({'sub' : user.username})
    refresh_token = oauth2.create_token({'sub' : user.username}, timedelta(weeks=1))

    user.refresh_token = refresh_token
    db.commit()

    return AuthResponse(
        access_token = access_token,
        request_token = refresh_token,
        token_type = 'bearer'
    )
    

def get_user_by_username(username : str, db: Session):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    return user
