from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import validates, relationship

from src.core.exceptions import ValidationError, EmailValidationError
from src.db.base import UUIDModel, TimeStampedModel
from src.security.password import hash_password, verify_password


class User(UUIDModel, TimeStampedModel):
    __tablename__ = "users_user"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @validates("first_name", "last_name")
    def validate_name(self, key, value):
        """Ensure first_name is not blank."""
        if not value or not value.strip():  # Remove spaces and check if empty
            raise ValidationError("First name or Last name cannot be blank")
        return value.lower().capitalize()

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise EmailValidationError()
        return email

    def set_password(self, password: str):
        self.hashed_password = hash_password(password)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)

    def __str__(self) -> str:
        return f"{self.email}"