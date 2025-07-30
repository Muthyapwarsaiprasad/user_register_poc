from pydantic import BaseModel, EmailStr,StringConstraints
from typing import Optional, Annotated
from datetime import datetime

PhoneStr = Annotated[str, StringConstraints(pattern=r'^\+?\d{10,15}$')]
PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=20)]

class RegisterUser(BaseModel):
    username: EmailStr | PhoneStr
    password: PasswordStr
    first_name: str
    last_name: str
    dob: datetime
    doj: datetime
    address: str
    comment: Optional[str] = None
    active: bool = True

class LoginModel(BaseModel):
    username: EmailStr | PhoneStr
    password: PasswordStr

class ChangePasswordModel(BaseModel):
    old_password: PasswordStr
    new_password: PasswordStr

class ForgotPasswordRequest(BaseModel):
    username: EmailStr | PhoneStr