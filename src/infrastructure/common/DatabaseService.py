import logging
import os
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src.common.exception.ExceptionFactory import ExceptionFactory
from src.common.utils.MessageFactory import MessageFactory
from src.infrastructure.common.enums.InfrastructureException import InfrastructureException
from src.infrastructure.common.enums.InfrastructureMessage import InfrastructureMessage


class DatabaseService:

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    __engine: Engine = None
    __sessionMaker: sessionmaker = None
    __session: Optional[Session] = None

    def __init__(self):
        self.__engine = self.__createEngine()
        self.__sessionMaker = self.__createSessionMaker()

    def __createEngine(self) -> Engine:
        return create_engine(self.DATABASE_URL)

    def __createSessionMaker(self) -> sessionmaker:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    def getSession(self) -> Session:
        if self.__session is None:
            self.__session = self.__sessionMaker()
        return self.__session

    def closeSession(self) -> None:
        if self.__session is not None:
            self.__session.close()
            self.__session = None

    def commitSession(self) -> None:
        if self.__session is not None:
            self.__session.commit()

    def rollbackSession(self) -> None:
        if self.__session is not None:
            self.__session.rollback()

    def checkConnection(self) -> bool:
        try:
            with self.getSession() as session:
                session.execute(text("SELECT 1"))
            print(MessageFactory
                  .type(InfrastructureMessage.SUCCESS_CONNECTION_DB)
                  .getMessage())

            return True

        except SQLAlchemyError:
            logging.error(ExceptionFactory
                          .type(InfrastructureException.ERROR_CONNECTION_DB)
                          .getMessage(), exc_info=True)
            return False
        finally:
            self.closeSession()
