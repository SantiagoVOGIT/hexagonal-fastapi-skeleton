from fastapi import FastAPI
from src.infrastructure.config.CorsConfig import CorsConfig
from src.infrastructure.common.DatabaseService import DatabaseService
from src.infrastructure.input_adapters.controllers.HealthController import HealthController


class Main:

    __app: FastAPI = None
    __dbConnection: DatabaseService = None
    __healthController: HealthController = None

    def __init__(self):
        self.__app = FastAPI()
        self.__dbConnection = DatabaseService()
        self.__healthController = HealthController(self.__dbConnection)

    def setupControllers(self) -> None:
        self.__healthController.setupRoutes(self.__app)

    def setupConfig(self) -> None:
        CorsConfig.setup(self.__app)

    def getApp(self) -> FastAPI:
        return self.__app

    @staticmethod
    def initialize() -> FastAPI:
        main = Main()
        main.setupConfig()
        main.setupControllers()
        return main.getApp()


app: FastAPI = Main.initialize()
