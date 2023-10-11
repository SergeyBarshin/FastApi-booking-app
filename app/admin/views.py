from sqladmin import ModelView

from app.bookings.models import Bookings
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "Категория"

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c]
    column_details_exclude_list = [Users.hashed_password]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"