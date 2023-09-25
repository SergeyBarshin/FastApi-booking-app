from app.dao.base import BaseDAO
from app.bookings.models import Bookings

from sqlalchemy import select

class BookingDAO(BaseDAO):
    model = Bookings

