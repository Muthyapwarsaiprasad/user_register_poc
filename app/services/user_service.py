from app.database.mongodb import users, tokens
from app.utils.password_utils import hash_password, verify_password
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    PasswordPolicyException,
    TooManyResetRequests,
    TokenExpiredException
)
from app.utils.password_utils import (
    hash_password,
    verify_password,
    is_strong_password
)
from datetime import datetime, date


async def register_user(data):
    # check duplicate user
    if users.find_one({"username": data.username}):
        raise UserAlreadyExistsException()
    
    # password strength check
    if not is_strong_password(data.password):
        raise PasswordPolicyException()
    
    data.password = hash_password(data.password)
    
    # Convert to dict
    doc = data.dict()
    
    doc["password_changed_at"] = datetime.utcnow()

    # insert into MongoDB
    users.insert_one(doc)

    return {"message": f"Successfully registered with username: {data.username}", "status":"success"}


    
    
