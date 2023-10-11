from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exсeptions import BookNotFound, RoomCanNotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=['Бронирования'],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    booking_dao = BookingDAO()
    result = await booking_dao.get_bookings_by_user_id(user_id=user.id)
    return result


@router.delete("/{id}")
async def delete_bookings(id: int, user: Users = Depends(get_current_user)):
    booking_dao = BookingDAO()
    books = await booking_dao.find_one_or_none(id=id)
    if not books:
        raise BookNotFound
    await booking_dao.delete_by_id(id=id)


@router.post("")
async def add_bookings(room_id: int,
                       date_from: date,
                       date_to: date,
                       user: Users = Depends(get_current_user),):
    booking_dao = BookingDAO()
    booking = await booking_dao.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBooked

    return booking
