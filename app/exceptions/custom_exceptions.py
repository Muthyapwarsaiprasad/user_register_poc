from fastapi import HTTPException, status

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User already exists")

class PasswordPolicyException(HTTPException):
    def __init__(self): super().__init__(status_code=422, detail="Weak password or reuse")

class  TooManyResetRequests (HTTPException):
     def __init__(self): super().__init__(status_code=429, detail="Too many reset requests")


class TokenExpiredException(HTTPException):
     def __init__(self): super().__init__(status_code=400, detail="Reset token expired or invalid")

