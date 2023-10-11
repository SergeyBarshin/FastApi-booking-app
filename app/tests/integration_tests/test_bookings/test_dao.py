import pytest
from app.bookings.dao import BookingDAO
from datetime import datetime

async def test_add_and_get_bookings():
    booking_dao = BookingDAO()
    new_booking = await booking_dao.add(
        user=2, 
        room_id=2, 
        date_from=datetime.strptime("2023-07-10","%Y-%m-%d"), 
        date_to=datetime.strptime("2023-07-24","%Y-%m-%d"), 
        )


    assert new_booking[0]['Bookings'].user_id == 2
    assert new_booking[0]['Bookings'].room_id == 2

    new_booking = await booking_dao.find_by_id(new_booking[0]['Bookings'].id)

    assert new_booking is not None