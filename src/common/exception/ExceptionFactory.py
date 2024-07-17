from enum import Enum


class CustomException(Exception):

    __errorCode: str = None
    __errorMessage: str = None

    def __init__(self, errorType: Enum):
        self.__errorCode = errorType.name
        self.__errorMessage = errorType.value

    def getCode(self) -> str:
        return self.__errorCode

    def getMessage(self) -> str:
        return self.__errorMessage


class ExceptionFactory:

    @staticmethod
    def type(errorType: Enum) -> CustomException:
        return CustomException(errorType)
