from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dao.users_dao import UserDAO
from src.db.deps import get_db_session
from src.security.jwt import decode_access_token


class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        from fastapi import status

        try:
            r = await super().__call__(request)
            token = r.credentials
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            token = None
        return token


optional_auth_scheme = OptionalHTTPBearer()
auth_scheme = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Extract the current user from the JWT token.
    :param token: JWT token from the request.
    :param db: Database session.
    :return: User object if valid, otherwise raises an HTTPException.
    """
    token_data = decode_access_token(token.credentials)
    user = await UserDAO.get_user_by_email(db, token_data["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
