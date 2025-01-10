import structlog
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from src.bot.models.base import BaseOrm
from src.bot.utils.pg_session import get_pg_session


class BaseRepository:
    __abstract__ = True

    def __init__(self, model: type[BaseOrm]):
        self.__model__ = model
        self.logger = structlog.get_logger(__name__)

    async def get_by_id(self, **kwargs):
        async with get_pg_session() as session:
            try:
                result = await session.execute(select(self.__model__).filter_by(**kwargs))
                return result.scalars().first()
            except Exception as e:
                self.logger.error(f"Error fetching entity by id", kwargs=kwargs, error=str(e))
                return None

    async def get_by_params(self, **kwargs):
        async with get_pg_session() as session:
            query = select(self.__model__)
            if kwargs:
                self.logger.info("Found record by params", params=kwargs)
                query = query.filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar()

    async def save(self, data):
        async with get_pg_session() as session:
            session.add(data)
            await session.commit()
            self.logger.info("Data saved", data=data)
            return data

    async def update(self, telegram_id: int, **kwargs):
        """
        Updating filed in your model.

        :param telegram_id: User telegram id to update.
        :param kwargs: Any field.
        :return:
        """
        async with get_pg_session() as session:
            user = await self.get_by_telegram_id(telegram_id)
            if not user:
                return
            try:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                session.add(user)
                await session.commit()
            except Exception as e:
                await session.rollback()
                self.logger.error(f"Error while updating {key} for user id: {user.id}", detail=e)
        return user

    async def get_by_telegram_id(self, telegram_id: int):
        async with get_pg_session() as session:
            try:
                result = await session.execute(select(self.__model__).filter_by(telegram_id=telegram_id))
                user = result.scalar_one_or_none()
                if not user:
                    self.logger.error(f"User with id: {telegram_id} not found.")
                    return None
                return user
            except Exception as e:
                self.logger.error("Error when trying to finding user", detail=e)
                return None

    async def delete_by_id(self, entity_id: int):
        async with get_pg_session() as session:
            await session.execute(delete(self.__model__).filter_by(id=entity_id))

    async def get_by_ids(self, ids):
        async with get_pg_session() as session:
            result = session.execute(select(self.__model__).filter(self.__model__.id.in_(ids))).fetchall()
            return result.scalars().all()

    async def get_list(self):
        async with get_pg_session() as session:
            try:
                records = await session.execute(select(self.__model__))
                records_list = records.scalars().all()
                self.logger.info(f"Found {len(records_list)} records in {self.__model__}")
                return records_list
            except SQLAlchemyError as e:
                self.logger.error("Error while fetching records", exc_info=True, detail=e)
                return None
