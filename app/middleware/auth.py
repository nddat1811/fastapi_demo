
from app.auth.oauth2 import get_current_user
from urllib.request import Request
from app.db.db_function import is_authentication
from app.models.user import SysUser
from app.utils.helper import is_path_not_check_authentication
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import  HTTPException, status

async def check_authentication(request: Request, db: Session, original_path: str):
    if(is_path_not_check_authentication(original_path)):
        return True

    else:
        try:
            token = request.headers.get('Authorization').split(" ")[1]
            current_user: SysUser = await get_current_user(token, db)
            is_authorized = await is_authentication(current_user.id, original_path, db)
            return is_authorized  # return True if authenticated, otherwise False
        except Exception as e:
            print("zo wwtfffffffffff")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="TESST token")  # return False if token is invalid or expired
            return False