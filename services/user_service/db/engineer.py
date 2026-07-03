import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()


from loguru import logger


class DbEngine:
    """Настройки базы данных и подключения к ней."""

    def __init__(self):
        self.db_url: str = os.getenv("DB_CONNECTION")  # type: ignore
        self.engine = create_engine(
            self.db_url,
            echo=False,
            isolation_level="READ COMMITTED",
            pool_size=20,
            max_overflow=0,
            pool_recycle=1800,
        )

        self.SessionLocal = scoped_session(
            sessionmaker(autoflush=False, bind=self.engine)
        )

    @contextmanager
    def get_session(self):
        try:
            session = self.SessionLocal()
            yield session
            session.commit()
        except Exception as e:
            logger.exception("Can't accomplish transaction. Rollback...", exc_info=e)
            session.rollback()
            raise
        finally:
            session.close()
            self.SessionLocal.remove()
