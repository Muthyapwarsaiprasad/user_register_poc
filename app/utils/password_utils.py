from passlib.context import CryptContext
import re

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_content.hash(password)

def verify_password(plain:str, hashed:str) -> bool:
    return pwd_content.verify(plain, hashed)

def is_strong_password(p: str) -> bool:
    return (8 <= len(p) <= 20
            and re.search(r"[A-Z]",p)
            and re.search(r"[a-z]", p)
            and re.search(r"[0-9]", p)
            and re.search(r"[!@#$%^&*(),._+=-?/:|]",p))