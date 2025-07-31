from pydantic import BaseModel

class MessageModel(BaseModel):
    message: str
    status: str

class TokenModel(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"