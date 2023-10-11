import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code",[
    ("test@test.com", "test", 200),
    ("test@test.com", "test01", 409),
    ("abcde", "pesokot", 422),

])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    responce = await ac.post("auth/register", json={
        "email": email,
        "password": password,
    })

    assert responce.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("fedor@moloko.ru", "tut_budet_hashed_password_1", 200),
    ("artem@example.com", "artem", 200),
    ])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    responce = await ac.post("auth/login", json={
        "email": email,
        "password": password,
    })

    assert responce.status_code == status_code
