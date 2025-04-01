from sqlalchemy import Column, Integer, ForeignKey, Text, UUID
from sqlalchemy.orm import relationship

from src.db.base import UUIDModel, TimeStampedModel


class Post(UUIDModel, TimeStampedModel):
    __tablename__ = "posts_post"

    user_id = Column(UUID, ForeignKey("users_user.id"), nullable=False)
    text = Column(Text, nullable=False)

    user = relationship("User", back_populates="posts")