from sqlalchemy import and_, func, insert, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    async def add(self, user, room_id, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
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
            ).cte('booked_rooms')

            get_rooms_left = select((Rooms.quantity - func.count(booked_rooms.c.room_id)
                                ).label('rooms_left')).select_from(Rooms).join(
                                    booked_rooms, booked_rooms.c.room_id == Rooms.id
                                ).where(Rooms.id == room_id).group_by(
                                    Rooms.quantity, booked_rooms.c.room_id
                                )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = len(rooms_left.mappings().all())

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()

                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().all()
            else:
                return None

    async def get_bookings_by_user_id(self, user_id):
        async with async_session_maker() as session:
            query = select(Bookings.__table__.columns
                           ).filter(Bookings.user_id == user_id)

            result = await session.execute(query)
            return result.mappings().all()
