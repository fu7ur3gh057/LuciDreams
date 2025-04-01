from typing import AsyncGenerator

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from taskiq import TaskiqDepends

from src.core.settings import settings


async def get_db_session(request: Request = TaskiqDepends()) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get async database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()


def get_sync_engine() -> Engine:
    return create_engine(
        settings.DATABASE_URL,
        pool_size=5,
        max_overflow=20
    )
