from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)

class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels")
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    stars: Optional[int] = Query(None, ge=1, le=5),
    has_spa: Optional[bool] = None
) -> list[SHotel]:

    hotels = [ 
        {
            "address": "ул. Гагарина, 1, Алтай",
            "name": "Super Hotel",
            "stars": 5,
        },
    ]

    return hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/booking")
def add_booking(booking: SBooking):
    pass
