import inspect
from time import time
from functools import wraps
from app.log.user_logger import get_logger
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_handler import verify_access_token
from app.database.mongodb import users
from datetime import datetime
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

logger = get_logger('user_log_execution_time')

def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time()
        try:
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            execution_time_ms = round((time() - start_time) * 1000, 2)
            logger.info(f"{func.__name__} executed in {execution_time_ms} ms")
            return result

        except HTTPException as http_exc:
            logger.warning(f"Handled HTTPException in {func.__name__}: {http_exc.status_code} - {http_exc.detail}")
            raise http_exc

        except Exception as e:
            logger.exception(f"Unexpected exception in {func.__name__}: {str(e)}")
            raise e

    return wrapper


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    try:
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        user = users.find_one({"_id":ObjectId(user_id)})
        if not user:
           raise HTTPException(status_code=404, detail="User not found")
        
        # Optional: Password expiration logic
        if user.get("password_changed_at"):
            if isinstance(user["password_changed_at"], datetime):
                if (datetime.utcnow() - user["password_changed_at"]).days >= 30:
                   raise HTTPException(status_code=403, detail="Password expired")
        return user
    
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
