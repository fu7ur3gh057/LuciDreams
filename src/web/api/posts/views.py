from typing import List
from uuid import UUID

from cachetools import TTLCache
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DAOException
from src.db.dao.posts_dao import PostDAO
from src.db.deps import get_db_session
from src.db.models.users_model import User
from src.security.deps import get_current_user
from src.web.api.posts.schemas import PostResponseSchema, PostCreateSchema

router = APIRouter()

posts_cache = TTLCache(maxsize=1000, ttl=300)


@router.post("/", response_model=PostResponseSchema)
async def add_post(
        payload: PostCreateSchema,
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user),
):
    if len(payload.text.encode("utf-8")) > 1_000_000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Post text exceeds 1MB limit."
        )
    try:
        post = await PostDAO.create_post(session, user_id=current_user.id, text=payload.text)
        posts_cache.pop(current_user.id, None)  # invalidate cache
        print("CACHED!")
        return post
    except DAOException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=List[PostResponseSchema])
async def get_posts(
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user),
):
    if current_user.id in posts_cache:
        return posts_cache[current_user.id]

    try:
        posts = await PostDAO.get_posts_by_user(session, user_id=current_user.id)
        posts_cache[current_user.id] = posts
        return posts
    except DAOException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user),
):
    success = await PostDAO.delete_post_by_id(session, post_id=post_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or unauthorized."
        )
    posts_cache.pop(current_user.id, None)  # invalidate cache
