import pytest

from app.users.dao import UserDao


@pytest.mark.parametrize("user_id,email,is_present", [
    (1, "fedor@moloko.ru", True),
    (2, "sharik@moloko.ru", True),
    (30, "fafafafa", False),
])
async def test_find_user_by_id(user_id, email, is_present):
    users_dao = UserDao()
    user = await users_dao.find_by_id(user_id)

    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
