
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.auth.oauth2 import RoleChecker, get_current_user
from app.models import user
from app.models.user import DbUser
from app.schemas.user import CheckCodePasswordRequest, ForgotPasswordRequest, UpdateRoleRequest, UpdateUserRequest, User2Base, User3Base, UserDisplay, UserResetPasswordRequest, ResetPasswordResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import db_user
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.utils.constants import Role
from app.utils.helper import generate_code

router = APIRouter(
    prefix='/users',
    tags=['User']
)
templates = Jinja2Templates(directory="app/resources/templates")

conf = ConnectionConfig(
    MAIL_USERNAME = "testpython18mmt@gmail.com",
    MAIL_PASSWORD = "egya xsda ulcb zdfx",
    MAIL_FROM = "testpython18mmt@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="python test",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


@router.get('/', response_model = List[UserDisplay])
async def get_all_users(db : Session = Depends(get_db), _ : bool = Depends(RoleChecker(allowed_roles=[Role.ADMIN, Role.STAFF]))):
    return db.query(DbUser).all()

@router.get('/{id}', response_model = UserDisplay)
async def get_user_by_id(id : int, db : Session = Depends(get_db), _ : DbUser = Depends(get_current_user)): 
    return await db_user.get_user_by_id(db, id)

#thiếu get profile

@router.put('/current_user', response_model=UserDisplay)
async def update_current_user(update_user_request: UpdateUserRequest, db : Session = Depends(get_db),  current_user : DbUser = Depends(get_current_user)):
    return await db_user.update_current_user(update_user_request, current_user, db)

@router.delete('/{id}')
async def delete_user( id: int, db: Session = Depends(get_db), _: bool = Depends(RoleChecker([Role.ADMIN]))):
    return await db_user.delete_user(id, db)

@router.put('/role/{id}', response_model=UserDisplay)
async def edit_role(update_role_request : UpdateRoleRequest, id : int, db : Session = Depends(get_db), _ : bool = Depends(RoleChecker(allowed_roles=[Role.ADMIN]))):
    return await db_user.update_role(update_role_request, id, db)


# Forgot password
@router.post('/forgot-password', response_model= ResetPasswordResponse)
async def forgot_password(req: ForgotPasswordRequest = None, db: Session = Depends(get_db)):
    user =  await db_user.get_user_by_email(db, req.email) # find the user with the gmail
    if user is None:
        return user
    # Generate code code (string: 6 digits random)
    code = generate_code()
    user_reset_password = await db_user.save_code(db, code, user.id) 
    if user_reset_password is None:
        return user_reset_password

    # Path to file template forgot.html
    template_file = "forgot.html"
    # Pass variable for template
    context = {"user": user, "code": code}
    # Render template from file and return HTML
    html = templates.TemplateResponse(template_file, {"request": req, **context})

    message = MessageSchema(
        subject="This mail ",
        recipients=[req.email],
        body=html.body,
        subtype=MessageType.html)

    fast_mail = FastMail(conf)
    await fast_mail.send_message(message)
    return user_reset_password

@router.post('/check-code-password', response_model= ResetPasswordResponse)
async def check_code_password(req: CheckCodePasswordRequest, db: Session = Depends(get_db)):
    user = await db_user.check_code_password(db, req.code)
    return user

@router.post('/reset-password', response_model= ResetPasswordResponse)
async def reset_password(req: UserResetPasswordRequest, db: Session = Depends(get_db)):
    if req.new_pass != req.conf_pass:
        return "Invalid"
    # Temporary use user_id pass in form
    user =  await db_user.reset_password(db, req.new_pass, req.user_id)
    return user
    
