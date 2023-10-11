from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    async def get_all(self, location, date_from, date_to):

        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter_by(location=location)
            result = await session.execute(query)
            hotels = list(result.mappings().all())
            res = []

            for hotel in hotels:
                engaged_rooms_query = select(func.count(Bookings.room_id).label('rooms_left')
                                        ).select_from(Bookings).join(
                                        Rooms, Rooms.id == Bookings.room_id
                                        ).where(
                                            and_(
                                                Rooms.hotel_id == hotel.id,
                                                or_(
                                                    and_(
                                                        Bookings.date_from >= date_from,
                                                        Bookings.date_from <= date_to
                                                    ),
                                                    and_(
                                                        Bookings.date_from <= date_from,
                                                        Bookings.date_to > date_from
                                                    ),
                                                ) 
                                            )
                                        )
                rooms_engaged = await session.execute(engaged_rooms_query)
                rooms_engaged: int = rooms_engaged.scalar()

                tmpDict = dict(hotel)
                tmpDict['rooms_left'] = tmpDict['rooms_quantity'] - rooms_engaged
                res.append(tmpDict)

        return res        