from fastapi import APIRouter, Depends, Response

from app.exсeptions import IncorrectEmailOrPassword, UserAlreadyExistsException
from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.dao import UserDao
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth && Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    user_dao = UserDao()
    existing_user = await user_dao.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    else:
        hashed_password = get_password_hash(user_data.password)
        await user_dao.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    access_tocken = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_tocken", access_tocken, httponly=True)
    return access_tocken


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_tocken")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
