from enum import Enum


class InfrastructureException(Enum):

    ERROR_CONNECTION_DB = "Error en la conexión a la base de datos. Revise los logs del servidor para más detalles."
    ENV_DB_NOT_SET = "No se ha configurado la URL de la base de datos en las variables de entorno"
