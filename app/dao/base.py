from app.database import async_session_maker
from sqlalchemy import select, insert

class BaseDAO:
    model = None

    async def find_by_id(self, model_id: int):
        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter_by(id = model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    async def find_one_or_none(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    async def find_all(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        
    async def add(self, **data):
        async with async_session_maker() as session:
            query = insert(self.model).values(**data)
            await session.execute(query)
            await session.commit()