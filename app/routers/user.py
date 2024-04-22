from fastapi import APIRouter, Depends
from app.schemas.user import EmailResetPasswordRequest, OTPResetPasswordRequest, UserResetPasswordRequest, ResetPasswordResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import db_user
from fastapi.templating import Jinja2Templates
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


# Forgot password
@router.post('/forgot-password', response_model= ResetPasswordResponse)
async def forgot_password(req_email: EmailResetPasswordRequest = None, db: Session = Depends(get_db)):
    user =  await db_user.get_user_by_email(db, req_email.email) # find the user with the gmail
    if user is None:
        return user
    # Generate code otp (string: 6 digits random)
    code = generate_otp()
    user_reset_password = await db_user.save_otp(db, code, user.id) 
    if user_reset_password is None:
        return user_reset_password

    # Path to file template forgot.html
    template_file = "forgot.html"
    # Pass variable for template
    context = {"user": user, "code": code}
    # Render template from file and return HTML
    html = templates.TemplateResponse(template_file, {"request": req_email, **context})

    message = MessageSchema(
        subject="This mail ",
        recipients=[req_email.email],
        body=html.body,
        subtype=MessageType.html)

    fast_mail = FastMail(conf)
    await fast_mail.send_message(message)
    return user_reset_password

@router.post('/check-otp-password', response_model= ResetPasswordResponse)
async def check_otp_password(req_code: OTPResetPasswordRequest, db: Session = Depends(get_db)):
    user = await db_user.check_otp_password(db, req_code.code)
    return user

@router.post('/reset-password', response_model= ResetPasswordResponse)
async def reset_password(req: UserResetPasswordRequest, db: Session = Depends(get_db)):
    if req.new_pass != req.conf_pass:
        return "Invalid"
    # Temporary use user_id pass in form
    user =  await db_user.reset_password(db, req.new_pass, req.user_id)
    return user
    
