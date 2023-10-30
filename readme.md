uvicorn app.main:app --reload

sqlalchemy - orm
dao - data acces obj

_alembic_ миграции

- alembic revision --autogenerate -m "Initial migrations" # создание миграции
- alembic upgrade head # применение миграции
- alembic downgrade -1 # отмена 1 миграции

_redis_

- команда для установки библиотеки `pip install "fastapi-cache2[redis]"`

_Сортировака импортов_

- isort app/main.py

_Sentry - трекинг ошибок_

_DOCKER_

- pip freeze > requirements.txt
- docker build .
- docker run -p 9000:8000 HASH_ID
