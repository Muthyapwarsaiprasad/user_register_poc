from app.database.mongodb import users
from app.utils.password_utils import verify_password
from app.utils.jwt_handler import create_access_token
from fastapi import HTTPException

async def user_login(username: str, password: str):
    # Directly match "username" as stored in MongoDB
    user = users.find_one({"username": username})
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username. Please try again.")

    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password. Please try again.")

    token = create_access_token({"user_id": str(user["_id"])})
    return {
        "message": f"Successfully logged in with Username: {username}",
        "access_token": token,
        "token_type": "bearer"
    }
