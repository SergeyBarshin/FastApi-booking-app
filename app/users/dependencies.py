from fastapi import Request, Depends
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.dao import UserDao
from app.exсeptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatExeption, UserIsNotPresent

def get_token(request: Request):
    tocken = request.cookies.get("booking_access_tocken")
    if not tocken:
        raise TokenAbsentException
    return tocken

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload =  jwt.decode(token, settings.SECRET_KEY, settings.ALGORITM)
    except JWTError:
        raise IncorrectTokenFormatExeption
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) <  datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresent
    
    user_dao = UserDao()
    user = await user_dao.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresent
    return user

