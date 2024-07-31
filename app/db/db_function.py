from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.function import SysFunction
from app.models.role import SysRole, SysRoleFunction
from app.models.user import SysUserRole
from ..auth import oauth2
from app.schemas.authentication import AuthResponse, RegistrationRequest
from app.schemas.user import UpdateUserRequest
from . import hash
from datetime import timedelta, datetime
from app.models import SysUser


async def is_authentication(user_id: int, url: str, db : Session):
    auth_query = (
        db.query(SysUser)
        .join(SysUserRole, SysUser.id == SysUserRole.user_id)
        .join(SysRole, SysUserRole.role_id == SysRole.id)
        .join(SysRoleFunction, SysRole.id == SysRoleFunction.role_id)
        .join(SysFunction, SysRoleFunction.function_id == SysFunction.id)
        .filter(
            SysUser.id == 2,
            SysFunction.path == url
        ).first()
    )
    return auth_query is not None