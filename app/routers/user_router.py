from fastapi import APIRouter, HTTPException
from app.models.request_schema import (
    RegisterUser, LoginModel, ChangePasswordModel, ForgotPasswordRequest
)
from app.models.response_schema import MessageModel, TokenModel
from app.services.user_service import (
    register_user
)
from app.exceptions.custom_exceptions import (
    userAlreadyExistsException, PasswordPolicyException, TokenExpiredException, TooManyResetRequests,
    user_already_exists_exception,password_policy_exception,token_expired_exception,too_many_reset_requests
)
from app.log.user_logger import get_logger
from app.utils.decorators import log_execution_time, get_current_user

router = APIRouter()
logger = get_logger("User_Registration_Module")

# User Register
@router.post("/register", response_model=MessageModel)
@log_execution_time
async def register(user: RegisterUser):
    try:
        register_user(user)
        logger.info(f"Successfully Registered with {user.username}")
        return {"message": f"Successfully Registered with {user.username}", "status": True}
    except userAlreadyExistsException:
        logger.exception(user_already_exists_exception())
        raise user_already_exists_exception()
    except HTTPException:
        raise HTTPException(status_code=500, detail="User is failed to register. please try again.")
