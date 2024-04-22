from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.schemas.user import UserResetPassword
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.oauth2 import get_current_user
from app.db import db_user
from fastapi.templating import Jinja2Templates
from ..schemas.user import RegistrationRequest, UserBase
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.utils.otp import generate_otp



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


@router.post('/register', response_model = UserBase)
async def register(registration_request : RegistrationRequest, db : Session = Depends(get_db)):
    return db_user.create_new_user(registration_request, db)

@router.get('/secure')
def secure(user = Depends(get_current_user)):
    return "sad"

# Forgot password
@router.post('/forgot-password')
async def forgot_password(request: Request, email: str = None, db: Session = Depends(get_db)):
    print(f"request {request} and email {email}")
    user =  await db_user.get_user_by_email(db, email) # find the user with the gmail
    if user is None:
        return None
        
    # Generate code otp (string: 6 digits random)
    code = generate_otp()
    user_reset_password = await db_user.save_otp(db, code, user.id) 
    if user_reset_password is None:
        return None

    # Path to file template forgot.html
    template_file = "forgot.html"
    # Pass variable for template
    context = {"user": user, "code": code}
    # Render template from file and return HTML
    html = templates.TemplateResponse(template_file, {"request": request, **context})

    message = MessageSchema(
        subject="This mail ",
        recipients=[email],
        body=html.body,
        subtype=MessageType.html)

    fast_mail = FastMail(conf)
    await fast_mail.send_message(message)
    return user_reset_password

#
@router.post('/check-otp-password')
async def check_otp_password(code: str, db: Session = Depends(get_db)):
    user = await db_user.check_otp_password(db, code)
    if user is None:
        return "Invalid otp or otp is expired"
    return user

@router.post('/reset-password')
async def reset_password(req: UserResetPassword, db: Session = Depends(get_db)):
    if req.new_pass != req.conf_pass:
        return "Invalid"
    
    # Temporary use user_id pass in form
    user =  await db_user.reset_password(db, req.new_pass, req.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUESTa, 
            detail="Reset pasword is error")
    return "reset password completed successfully"
    
