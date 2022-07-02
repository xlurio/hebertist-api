from abc import ABC, abstractmethod


class Game(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass
