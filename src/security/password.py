from passlib.context import CryptContext

import random
import string

from src.core.exceptions import PasswordValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password: str):
    if len(password) < 5:
        raise PasswordValidationError()


def hash_password(password: str) -> str:
    validate_password(password)
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def generate_verification_code():
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choices(characters, k=6))
