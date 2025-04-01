from asyncio import current_task
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from src.core.settings import settings


async def _setup_db(app: FastAPI) -> None:
    engine = create_async_engine(str(settings.ASYNC_DATABASE_URL), echo=False)
    session_factory = async_scoped_session(
        async_sessionmaker(
            engine,
            expire_on_commit=False,
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to set up database session factory.
    """
    await _setup_db(app)
    yield
    await app.state.db_engine.dispose()
