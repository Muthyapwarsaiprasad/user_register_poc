from pydantic import BaseModel

class MessageModel(BaseModel):
    message: str
    status: bool

class TokenModel(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"