from fastapi import HTTPException, status

class  userAlreadyExistsException  (HTTPException):
    """Exception raised when an user with same id already exists."""
    pass

class PasswordPolicyException(HTTPException):
     """Exception raised when an user Weak password or reuse."""
     pass

class  TooManyResetRequests (HTTPException):
    """Exception raised when too many reset requests."""
    pass

class TokenExpiredException(HTTPException):
    """Exception raised when Reset token expired or invalid."""
    pass


def user_already_exists_exception():
    return HTTPException (
        status_code = status.HTTP_400_BAD_REQUEST,
        detail = "username already exists."
    )

def password_policy_exception():
    return HTTPException (
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail = "It is Weak password or recreate strong password."
    )

def too_many_reset_requests():
    return HTTPException (
        status_code = status.HTTP_429_TOO_MANY_REQUESTS,
        detail = "Too many reset requests."
    )

def token_expired_exception():
    return HTTPException (
        status_code = status.HTTP_400_BAD_REQUEST,
        detail = "Reset token expired or invalid."
    )