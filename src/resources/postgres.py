from contextlib import asynccontextmanager

from dagster import ConfigurableResource
from loguru import logger
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.settings import settings


class PostgresResource(ConfigurableResource):
    connection_string: str

    async def session_maker(self):
        engine = create_async_engine(
            self.dsn,
            echo=not settings.IS_PRODUCTION,
        )
        return async_sessionmaker(bind=engine)

    async def get_db(self):
        session = await self.session_maker()
        db = session()
        try:
            yield db
        except DatabaseError as e:
            logger.exception(e)
            raise
        finally:
            await db.close()

    @asynccontextmanager
    async def get_db_ctx(self):
        session = await self.session_maker()
        db = session()
        try:
            yield db
        except DatabaseError as e:
            logger.exception(e)
            raise
        finally:
            await db.close()
