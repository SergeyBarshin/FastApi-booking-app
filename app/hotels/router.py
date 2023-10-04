from fastapi import APIRouter
from datetime import date
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels
from fastapi_cache.decorator import cache
import asyncio

router = APIRouter(
    prefix="/hotels",
    tags=['Отели'],
)

@router.get("/id/{id}")
async def get_hotels_by_id(
    id: int,
) -> list[SHotels]:
    
    hotels_dao = HotelDAO()
    result = await hotels_dao.find_all(id=id)
    return result


@router.get("/{location}")
@cache(expire=20) # ответ кешируется в редис
async def get_hotels_by_location_and_params(
    location: str,
    date_from: date,
    date_to: date,
) -> list[SHotels]:
    
    hotels_dao = HotelDAO()
    result = await hotels_dao.get_all(location=location, date_from=date_from, date_to=date_to)

    return result
