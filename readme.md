uvicorn app.main:app --reload

sqlalchemy - orm
dao - data acces obj

_alembic_ миграции
alembic revision --autogenerate -m "Initial migrations" # создание миграции
alembic upgrade head # применение миграции
alembic downgrade -1 # отмена 1 миграции
