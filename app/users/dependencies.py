from fastapi import HTTPException, Request, status, Depends
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.dao import UserDao

def get_token(request: Request):
    tocken = request.cookies.get("booking_access_tocken")
    if not tocken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return tocken

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload =  jwt.decode(token, settings.SECRET_KEY, settings.ALGORITM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) <  datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='3')
    
    user_dao = UserDao()
    user = await user_dao.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='4')

    return user