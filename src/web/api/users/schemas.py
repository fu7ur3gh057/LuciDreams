from uuid import UUID

from pydantic import BaseModel, EmailStr


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True
