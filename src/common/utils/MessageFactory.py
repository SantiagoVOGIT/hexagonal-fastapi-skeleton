from enum import Enum


class Message:

    __code: str = None
    __message: str = None

    def __init__(self, messageType: Enum):
        self.__code = messageType.name
        self.__message = messageType.value

    def getCode(self) -> str:
        return self.__code

    def getMessage(self) -> str:
        return self.__message


class MessageFactory:
    @staticmethod
    def type(messageType: Enum) -> Message:
        return Message(messageType)
