import uuid

from sqlalchemy import Column, DateTime, func, UUID
from sqlalchemy.orm import DeclarativeBase

from src.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta


class UUIDModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimeStampedModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


from src.db.models import (
    users_model,
    posts_model,
)
