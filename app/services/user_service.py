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
from datetime import datetime, date, timedelta

from fastapi import HTTPException
import uuid


MAX_RESET = 3
TOKEN_TTL_HOURS = 24

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


async def user_change_password(user, old_password, new_password):
    users.find_one({"_id":user})

    # verify old password
    if not verify_password(old_password, user["password"]):
        raise PasswordPolicyException()

    # new_password is strong password
    if not is_strong_password(new_password):
        raise PasswordPolicyException()

    # verify new_password
    if verify_password(new_password, user["password"]):
        raise PasswordPolicyException
    
    new_h = hash_password(new_password)
    users.update_one(
        {"_id":user["_id"]},
        {"$set": {"password":new_h, "password_changed_at": datetime.utcnow()}}
    )
    return {"message": "Successfully password changed", "status": "success"}

# generate_reset_token for username of forgot password
async def generate_reset_token(username):
    user_id = users.find_one({"username":username})

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    record = tokens.find_one({"username":username})
    if record and record.get("count", 0) >= MAX_RESET and record["created_at"] > datetime.utcnow() - timedelta(hours=TOKEN_TTL_HOURS):
        raise TooManyResetRequests()
    
    token = str(uuid.uuid4())
    tokens.update_one(
        {"username": username},
        {"$set":{
            "token": token,
            "created_at":datetime.utcnow(),
            "count":(record.get("count", 0) + 1) if record else 1
        }},
        upsert=True
    )
    return token

# confirm_reset_token for username of forgot password
async def confirm_reset_token(username, token, new_password):
    record = tokens.find_one({"username":username})
    if not record or record["token"] != token or record["created_at"] < datetime.utcnow() - timedelta(hours=TOKEN_TTL_HOURS):
        raise TokenExpiredException()
    
    if not is_strong_password(new_password):
        raise PasswordPolicyException()
    
    new_h = hash_password(new_password)
    users.update_one(
        {"username":username},
        {"$set":{
            "password":new_h,
            "password_changed_at":datetime.utcnow()
        }}
    )
    tokens.delete_one({"username":username})
    return {"message": "Successfully password reset", "status": "success"}