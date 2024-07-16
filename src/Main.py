from typing import Dict
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from common.utils.MessageFactory import MessageFactory, Message
from src.infrastructure.common.InfrastructureMessage import InfrastructureMessage
from src.infrastructure.config.CorsConfig import CorsConfig
from src.infrastructure.config.DatabaseService import DatabaseService
from src.infrastructure.common.InfrastructureException import InfrastructureException
from common.exception.ExceptionFactory import ExceptionFactory
from src.infrastructure.config.Environments import Environments


app: FastAPI = FastAPI()
dbConnection: DatabaseService = DatabaseService()


class Main:

    @staticmethod
    def setupRoutes() -> None:

        @app.get("/")
        async def apiStatus() -> Dict[str, str]:
            return {"message": f"Fine, current environment API: {Environments.getCurrentEnvironment()}"}

        @app.get("/health-database")
        async def healthDatabase(db: Session = Depends(dbConnection.generateDbSession)) -> Dict[str, str]:
            if not dbConnection.testConnection():
                raise HTTPException(
                    status_code=500,
                    detail=ExceptionFactory.type(InfrastructureException.ERROR_CONNECTION_DB).getMessage()
                )
            return {"message": MessageFactory.type(InfrastructureMessage.SUCCESS_CONNECTION_DB).getMessage()}

    @staticmethod
    def setupConfig() -> None:
        CorsConfig.setup(app)


Main.setupConfig()
Main.setupRoutes()
