from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from app.models.request_schema import (
    RegisterUser, LoginModel, ChangePasswordModel, ForgotPasswordRequest
)
from app.models.response_schema import MessageModel, TokenModel
from app.services.user_service import (
    register_user, user_change_password, generate_reset_token
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


# change-password
@router.post("/change-password", response_model=MessageModel)
@log_execution_time
async def change_password(user: ChangePasswordModel, current=Depends(get_current_user)):
    try:
        response = await user_change_password(current,user.old_password, user.new_password)
        logger.info(f"Successfully changed Password")
        return response
    
    except PasswordPolicyException as e:
        logger.warning(f"weak password. please try again: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Failed to change password : {str(e)}")
        raise HTTPException(status_code=500, detail="User failed to login. Please try again.")


# Forgot Password
@router.post("/forgot-password", response_model=MessageModel)
@log_execution_time
async def forgot_password(req: ForgotPasswordRequest, bg: BackgroundTasks):
    try:
        token = await generate_reset_token(req.username)

        # Simulate email sending in background
        bg.add_task(lambda: print(f"Email sent with token {token}"))

        logger.info(f"Reset token successfully generated for {req.username}")
        return {"message": "Reset token sent if user exists", "status": "success"}

    except TokenExpiredException as e:
        logger.warning(f"Too many token requests for {req.username}: {str(e)}")
        raise e

    except HTTPException as e:
        logger.warning(f"Handled HTTPException for {req.username}: {e.detail}")
        raise e  # Don't convert to 500 – return as-is

    except HTTPException as e:
        logger.error(f"Error during reset token generation for {req.username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during reset token generation.")  

# Reset password
@router.post("/reset-password", response_model=MessageModel)
async def reset_password(username:str, token:str, new_password:str):
    try:
        response = await generate_reset_token(username,token,new_password)
        logger.info(f"Successfully reset password for username {username}")
        return response
    
    except PasswordPolicyException as e:
        logger.warning(f"weak password. please try again: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Failed to reset password for user {username} : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to reset password for user {username}. Please try again.")
