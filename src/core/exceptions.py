from fastapi import HTTPException, status


class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class DAOException(AppException):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code, detail)


class ValidationError(HTTPException):
    """Base class for validation errors."""

    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class EmailValidationError(ValidationError):
    def __init__(self):
        super().__init__("Incorrect email format")


class PhoneValidationError(ValidationError):
    def __init__(self):
        super().__init__("Incorrect phone number format")


class PasswordValidationError(ValidationError):
    def __init__(self):
        super().__init__("Password must be at least 5 characters long")
