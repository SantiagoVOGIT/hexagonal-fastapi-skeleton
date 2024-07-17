from typing import Dict
from fastapi import FastAPI

from src.common.utils.MessageFactory import MessageFactory
from src.infrastructure.common.enums.InfrastructureMessage import InfrastructureMessage


class HealthController:

    @staticmethod
    def setupRoutes(app: FastAPI) -> None:
        @app.get("/")
        async def apiStatus() -> Dict[str, str]:
            return {"message": MessageFactory.type(InfrastructureMessage.CURRENT_ENVIRONMENT_API).getMessage()}
