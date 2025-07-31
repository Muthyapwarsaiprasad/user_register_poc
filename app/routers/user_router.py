from fastapi import APIRouter, HTTPException
from app.models.request_schema import (
    RegisterUser, LoginModel, ChangePasswordModel, ForgotPasswordRequest
)
from app.models.response_schema import MessageModel, TokenModel
from app.services.user_service import (
    register_user
)
from app.services.auth_service import user_login
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,PasswordPolicyException,TooManyResetRequests,TokenExpiredException
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
        response = await register_user(user)
        logger.info(f"Successfully registered with username: {user.username}")
        return MessageModel(**response)

    except (UserAlreadyExistsException, PasswordPolicyException) as e:
        logger.warning(f"Registration failed for {user.username}: {e.detail}")
        raise  # <-- already an HTTPException, just re-raise it

    except Exception as e:
        logger.error(f"User failed to register for {user.username}: {str(e)}")
        raise HTTPException(status_code=500, detail="User failed to register. Please try again.")

# User login
@router.post("/login", response_model=TokenModel)
@log_execution_time
async def login(user: LoginModel):
    try:
        response = await user_login(user.username, user.password)
        logger.info(f"Successfully logged in with username: {user.username}")
        return response

    except HTTPException as e:
        logger.warning(f"Login failed for {user.username}: {e.detail}")
        raise e

    except Exception as e:
        logger.error(f"Unexpected login failure for {user.username}: {str(e)}")
        raise HTTPException(status_code=500, detail="User failed to login. Please try again.")
# Login
# @router.post("/login", response_model=TokenModel)
# async def login_user(user: LoginModel):
#     response = await user_login(user.username, user.password)  # Await the coroutine
#     return response
