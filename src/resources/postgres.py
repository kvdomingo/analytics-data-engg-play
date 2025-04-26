from contextlib import contextmanager

from dagster import ConfigurableResource
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker

from src.settings import settings


class PostgresResource(ConfigurableResource):
    connection_string: str

    def session_maker(self):
        engine = create_engine(
            self.dsn,
            echo=not settings.IS_PRODUCTION,
        )
        return sessionmaker(bind=engine)

    def get_db(self):
        session = self.session_maker()
        db = session()
        try:
            yield db
        except DatabaseError as e:
            logger.exception(e)
            raise
        finally:
            db.close()

    @contextmanager
    def get_db_context(self):
        session = self.session_maker()
        db = session()
        try:
            yield db
        except DatabaseError as e:
            logger.exception(e)
            raise
        finally:
            db.close()
