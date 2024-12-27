from abc import ABC, abstractmethod
from rfeed import Feed
from logging import Logger
from pydantic import BaseModel

class AbstractOutput(ABC):

    @staticmethod
    @abstractmethod
    def execute(logger: Logger, feed: Feed, **kwargs) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_validator() -> BaseModel:
        pass