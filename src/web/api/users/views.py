from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dao.users_dao import UserDAO
from src.db.deps import get_db_session
from src.db.models.users_model import User
from src.security.deps import get_current_user
from src.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from src.web.api.users.schemas import (
    UserCreateSchema,
    LoginSchema,
    AccessTokenResponse,
    TokenResponseSchema,
    UserResponseSchema,
)

router = APIRouter()


# AUTH
@router.post("/register")
async def register(
        inp: UserCreateSchema, session: AsyncSession = Depends(get_db_session)
):
    user = await UserDAO.get_user_by_email(session, email=str(inp.email))
    if user:
        # User already created
        raise HTTPException(
            400,
            f"User with email {inp.email} already created"
        )
    else:
        # Creating new User model
        user = await UserDAO.create_user(session, **inp.model_dump())
        payload = {"sub": user.email, "user_id": str(user.id)}
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)

@router.post("/token/refresh", response_model=AccessTokenResponse)
async def refresh_access_token(token: str):
    payload = decode_refresh_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    new_access_token = create_access_token(
        {"sub": payload["sub"], "user_id": payload["user_id"]}
    )
    return AccessTokenResponse(access_token=new_access_token, token_type="bearer")


@router.post("/login", response_model=TokenResponseSchema)
async def login(inp: LoginSchema, session: AsyncSession = Depends(get_db_session)):
    user = await UserDAO.authenticate_user_by_email(
        session, email=str(inp.email), password=inp.password
    )
    payload = {"sub": user.email, "user_id": str(user.id)}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return None


# USERS
@router.get("/me", response_model=UserResponseSchema)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user
