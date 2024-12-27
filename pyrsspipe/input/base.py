from abc import ABC, abstractmethod
from rfeed import Feed
from logging import Logger
from pydantic import BaseModel


class AbstractInput(ABC):

    @staticmethod
    @abstractmethod
    def execute(logger: Logger, **kwargs) -> Feed:
        pass

    @staticmethod
    @abstractmethod
    def get_validator() -> BaseModel:
        pass
