from typing import Dict
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src.common.exception.ExceptionFactory import ExceptionFactory
from src.common.utils.MessageFactory import MessageFactory
from src.infrastructure.common.enums.InfrastructureException import InfrastructureException
from src.infrastructure.common.enums.InfrastructureMessage import InfrastructureMessage

from src.infrastructure.common.DatabaseService import DatabaseService
from src.infrastructure.config.Environments import Environments


class HealthController:

    __dbConnection: DatabaseService = None

    def __init__(self, dbConnection: DatabaseService):
        self.__dbConnection = dbConnection

    def setupRoutes(self, app: FastAPI) -> None:
        @app.get("/")
        async def apiStatus() -> Dict[str, str]:
            return {"message": f"Fine, current environment API: {Environments.getCurrentEnvironment()}"}

        @app.get("/health-database")
        async def healthDatabase(db: Session = Depends(self.__dbConnection.generateDbSession)) -> Dict[str, str]:
            if not self.__dbConnection.testConnection():
                raise HTTPException(
                    status_code=500,
                    detail=ExceptionFactory.type(InfrastructureException.ERROR_CONNECTION_DB).getMessage()
                )
            return {"message": MessageFactory.type(InfrastructureMessage.SUCCESS_CONNECTION_DB).getMessage()}
