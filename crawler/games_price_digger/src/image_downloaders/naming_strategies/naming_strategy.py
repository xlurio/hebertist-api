from abc import ABC, abstractmethod


class NamingStrategy(ABC):

    @abstractmethod
    def get_filename(self, extension) -> str:
        pass
