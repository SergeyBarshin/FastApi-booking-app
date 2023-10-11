from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    *[(4, "2030-05-01", "2030-05-15", 200)] * 8,
    ])
async def test_add_and_get_bookings(authenticated_ac: AsyncClient, room_id, date_from, date_to, status_code):
    responce = await authenticated_ac.get("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert responce.status_code == status_code
