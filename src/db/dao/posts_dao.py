from typing import Optional, List
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from src.db.models.posts_model import Post
from src.core.exceptions import DAOException


class PostDAO:
    @staticmethod
    async def create_post(db: AsyncSession, user_id: UUID, text: str) -> Post:
        post = Post(user_id=user_id, text=text)
        db.add(post)
        try:
            await db.commit()
            await db.refresh(post)
            return post
        except IntegrityError:
            await db.rollback()
            raise DAOException(status_code=400, detail="Could not create post")
        except Exception:
            await db.rollback()
            raise DAOException(status_code=500, detail="Internal server error")

    @staticmethod
    async def get_posts_by_user(db: AsyncSession, user_id: int) -> List[Post]:
        stmt = select(Post).where(Post.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def delete_post_by_id(db: AsyncSession, post_id: UUID, user_id: UUID) -> bool:
        stmt = delete(Post).where(Post.id == post_id, Post.user_id == user_id)
        try:
            result = await db.execute(stmt)
            await db.commit()
            return result.rowcount > 0
        except Exception:
            await db.rollback()
            raise DAOException(status_code=500, detail="Could not delete post")

    @staticmethod
    async def get_post_by_id(db: AsyncSession, post_id: UUID) -> Optional[Post]:
        stmt = select(Post).where(Post.id == post_id)
        result = await db.execute(stmt)
        return result.scalars().first()
