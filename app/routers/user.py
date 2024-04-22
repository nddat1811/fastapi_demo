from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.oauth2 import get_current_user
from ..db import db_user

from ..shemas.user import RegistrationRequest, UserBase


router = APIRouter(
    prefix='/users',
    tags=['User']
)
@router.post('/register', response_model = UserBase)
async def register(registration_request : RegistrationRequest, db : Session = Depends(get_db)):
    return db_user.create_new_user(registration_request, db)

@router.get('/secure')
def secure(user = Depends(get_current_user)):
    return "sad"