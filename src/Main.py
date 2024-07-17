from fastapi import FastAPI

from src.infrastructure.common.DatabaseService import DatabaseService
from src.infrastructure.config.CorsConfig import CorsConfig
from src.infrastructure.input_adapters.controllers.HealthController import HealthController


class Main:

    __app: FastAPI = None
    __dbService: DatabaseService = None
    __healthController: HealthController = None

    def __init__(self):
        self.__app = FastAPI()
        self.__dbService = DatabaseService()
        self.__healthController = HealthController()

    def ensureConnection(self) -> bool:
        return self.__dbService.checkConnection()

    def setupControllers(self) -> None:
        self.__healthController.setupRoutes(self.__app)

    def setupConfig(self) -> None:
        CorsConfig.setup(self.__app)

    def getApp(self) -> FastAPI:
        return self.__app

    @staticmethod
    def initialize() -> FastAPI:
        main = Main()
        main.ensureConnection()
        main.setupConfig()
        main.setupControllers()
        return main.getApp()


app: FastAPI = Main.initialize()
