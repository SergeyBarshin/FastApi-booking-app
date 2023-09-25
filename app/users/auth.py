from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from pydantic import EmailStr
from app.users.dao import UserDao
from ..config import settings

pwd_contex = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_contex.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_contex.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy ()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update ({"exp": expire})
    encoded_jwt = jwt.encode(
    to_encode,
    settings.SECRET_KEY, settings.ALGORITM)
    
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user_dao = UserDao()
    user =  await user_dao.find_one_or_none(email = email)
    if not user and not verify_password(password, user.password):
        return None
    return user
    
