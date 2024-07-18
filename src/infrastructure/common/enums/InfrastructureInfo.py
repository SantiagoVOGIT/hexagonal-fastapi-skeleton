from enum import Enum

from src.infrastructure.config.Environments import Environments


class InfrastructureInfo(Enum):

    SUCCESS_CONNECTION_DATABASE = "Conexión exitosa a la base de datos."
    CURRENT_ENVIRONMENT_API = f"Ambiente actual de la API: {Environments.getCurrentEnvironment()}."
