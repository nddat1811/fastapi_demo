from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.authentication import AuthResponse
from app.schemas.user import RegistrationRequest
from . import hash, oauth2
from datetime import timedelta, datetime
from app.models import DbUser

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

async def get_user_by_email(db: Session, email: str):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")
    return user

async def get_user_by_id(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {id} not found")
    return user


# Save OTP into reset password database
async def save_otp(db: Session, code: str, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with {user_id} not found")
    user.code = code
    user.expiry = datetime.now() + timedelta(minutes=1)
    db.commit()
    return user 

# Check if OTP is valid
async def check_otp_password(db: Session, code: str):
    user = db.query(DbUser).filter(DbUser.code == code).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with {code} not found")
    current_time = datetime.now()
    if current_time < user.expiry:
        return user
    else:
        return None

async def reset_password(db: Session, password: str, id: int):
    user = await get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with {id} not found")
    user.hashed_password = hash.Hash.bcrypt(password),
    db.commit()
    return user
