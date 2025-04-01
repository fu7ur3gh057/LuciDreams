from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.exceptions import DAOException
from src.db.models.users_model import User
from src.security.password import hash_password, verify_password


class UserDAO:
    @staticmethod
    async def create_user(
            db: AsyncSession,
            first_name: str,
            last_name: str,
            email: str,
            # phone: str,
            password: str,
    ) -> User:
        hashed_password = hash_password(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=hashed_password,
        )
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
            return user
        except IntegrityError:
            await db.rollback()
            raise DAOException(
                status_code=400, detail="User with this email already exists"
            )
        except Exception:
            await db.rollback()
            raise DAOException(status_code=500, detail="Internal server error")


    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        return user

    @staticmethod
    async def authenticate_user_by_email(
            db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        user = await UserDAO.get_user_by_email(db, email)
        if not user:
            raise DAOException(status_code=404, detail="User not found")
        if verify_password(password, user.hashed_password):
            return user
        raise DAOException(status_code=404, detail="Incorrect password")
