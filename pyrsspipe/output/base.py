from abc import ABC, abstractmethod
from rfeed import Feed
from logging import Logger

class AbstractOutput(ABC):
    @abstractmethod
    def execute(logger: Logger, feed: Feed, **kwargs) -> None:
        pass