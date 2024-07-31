
from app.auth.oauth2 import get_current_user
from urllib.request import Request
from app.db.db_function import is_authentication
from app.models.user import SysUser
from app.utils.helper import is_path_not_check_authentication
from sqlalchemy.orm import Session


async def check_authentication(request: Request, db: Session, original_path: str) -> bool:
    print("PATH: ", original_path)
    if(is_path_not_check_authentication(original_path)):
        print("authentication", )
        return True
    else:
        try:
            token = request.headers.get('Authorization').split(" ")[1]
            current_user: SysUser = await get_current_user(token, db)
            user_info = f"User: {current_user.id}"
            print("user_info:", user_info)
            t = is_authentication(current_user.id, original_path, db)
            print("user_infottttttt:", t)
            return True if t else False  # return True if authenticated, otherwise False
        except Exception as e:
            user_info = "User: Unauthenticated"
            return False
            # logger.error(f"Authentication error: {str(e)}")
       
    return False