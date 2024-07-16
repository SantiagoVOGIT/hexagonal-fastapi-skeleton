import os

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Generator, Optional

from common.exception.ExceptionFactory import ExceptionFactory
from src.infrastructure.common.InfrastructureException import InfrastructureException


class DatabaseService:

    __databaseUrl: str = None
    __engine: Engine = None
    __sessionLocal: sessionmaker = None

    def __init__(self) -> None:
        self.__databaseUrl = self.__getDatabaseUrl()
        self.__engine = self.__createEngine()
        self.__sessionLocal = self.__createSessionLocal()

    def __createEngine(self) -> Engine:
        return create_engine(
            self.__databaseUrl,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True
        )

    def __createSessionLocal(self) -> sessionmaker:
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.__engine
        )

    def generateDbSession(self) -> Generator[Session, None, None]:
        db = self.__sessionLocal()
        try:
            yield db
        finally:
            db.close()

    def testConnection(self) -> bool:
        try:
            with self.__engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as ex:
            print(f"Error de conexión: {str(ex)}")
            return False

    @staticmethod
    def __getDatabaseUrl() -> str:
        databaseUrl: Optional[str] = os.getenv("DATABASE_URL")

        if databaseUrl is None:
            raise ExceptionFactory.type(InfrastructureException.ENV_DB_NOT_SET).getMessage()
        return databaseUrl
