from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..auth import oauth2
from app.schemas.authentication import AuthResponse, RegistrationRequest
from app.schemas.user import UpdateUserRequest
from . import hash
from datetime import timedelta, datetime
from app.models import SysUser

async def create_new_user(registration_request : RegistrationRequest, db : Session) -> SysUser:
    
    if await get_user_by_username(registration_request.username, db):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='username already existed')
    
    if not await is_email_non_exist(registration_request.email, db):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='email already existed')

    user = SysUser(
        username = registration_request.username,
        hash_password = registration_request.password,
        email = registration_request.email,
        status = 1,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def is_email_non_exist(email: str, db : Session) -> bool:
    user = db.query(SysUser).filter(SysUser.email == email).first()
    return user is None

async def login(request : OAuth2PasswordRequestForm, db: Session) -> AuthResponse:
    user = await get_user_by_username(request.username, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    # if not hash.Hash.verify(request.password, user.hashed_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="invalid user"
    #     )
    
    claims = {'sub' : user.username}
    access_token = oauth2.create_token(claims)
    refresh_token = oauth2.create_token(claims, timedelta(weeks=1))

    user.refresh_token = refresh_token
    db.commit()

    return AuthResponse(
        access_token = access_token,
        request_token = refresh_token,
        token_type = 'bearer'
    )

async def refresh_token(token : str, db: Session) -> AuthResponse:
    username = oauth2.extract_claim(claim_type = 'sub', token=token)

    user = await get_user_by_username(username, db)

    if user is None: 
        raise oauth2.credentials_exception
    
    if token != user.refresh_token: 
        raise oauth2.credentials_exception
    
    claims = {'sub' : user.username, 'role' : user.role}
    access_token = oauth2.create_token(claims)
    refresh_token = oauth2.create_token(claims, timedelta(weeks=1))

    user.refresh_token = refresh_token
    db.commit()

    return AuthResponse(
        access_token = access_token,
        request_token = refresh_token,
        token_type = 'bearer'
    )
    

async def get_user_by_username(username : str, db: Session) -> SysUser | None:
    user = db.query(SysUser).filter(SysUser.username == username).first()
    return user

async def get_user_by_email(db: Session, email: str):
    user = db.query(SysUser).filter(SysUser.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")
    return user

async def get_user_by_id(db: Session, id: int):
    user = db.query(SysUser).filter(SysUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user

async def update_user(user_update_request : UpdateUserRequest, id : int, db : Session) -> SysUser:
    user = await get_user_by_id(db, id)
    user.role = user_update_request.role
    user.dob = user_update_request.dob
    db.commit()
    return user

async def delete_user(id : int, db : Session):
    user = await get_user_by_id(db, id)
    user.deleted_at = datetime.now()
    db.commit()

    return {
        "message" : f"Delete user {id} successfully"
    }


# Save OTP into reset password database
async def save_code(db: Session, code: str, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with {user_id} not found")
    user.code = code
    user.expiry = datetime.now() + timedelta(minutes=30)
    db.commit()
    return user 

# Check if code is valid
async def check_code_password(db: Session, code: str):
    user = db.query(SysUser).filter(SysUser.code == code).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with {code} not found")
    current_time = datetime.now()
    if current_time < user.expiry:
        user.code = None
        user.expiry = None
        db.commit()
        return user
    else:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=f"The code {code} is not available")

async def reset_password(db: Session, password: str, id: int):
    user = await get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with {id} not found")
    user.hashed_password = hash.Hash.bcrypt(password),
    db.commit()
    return user
