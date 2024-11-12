from abc import ABC, abstractmethod
from rfeed import Item, Feed
from logging import Logger


class AbstractInput(ABC):
    @abstractmethod
    def execute(logger: Logger, **kwargs) -> Feed:
        pass
