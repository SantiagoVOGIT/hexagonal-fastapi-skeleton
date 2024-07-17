from enum import Enum

from src.infrastructure.config.Environments import Environments


class InfrastructureMessage(Enum):

    SUCCESS_CONNECTION_DB = "Conexión exitosa a la base de datos."
    CURRENT_ENVIRONMENT_API = f"Current environment API: {Environments.getCurrentEnvironment()}"
