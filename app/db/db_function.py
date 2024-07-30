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
from app.utils.constants import Role
from . import hash
from datetime import timedelta, datetime
from app.models import SysUser


def is_authentication(user_id: int, url: str, db : Session) -> bool:
    auth_query = (
        db.query(SysUser)
        .join(SysUserRole, SysUser.id == SysUserRole.user_id)
        .join(SysRole, SysUserRole.role_id == SysRole.id)
        .join(SysRoleFunction, SysRole.id == SysRoleFunction.role_id)
        .join(SysFunction, SysRoleFunction.function_id == SysFunction.id)
        .filter(
            SysUser.id == user_id,
            SysFunction.path == url
        )
    )
    return auth_query is None