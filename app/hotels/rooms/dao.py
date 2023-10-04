from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker

class HotelDAO(BaseDAO):
    model = Rooms

    