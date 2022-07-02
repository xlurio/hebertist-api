from abc import ABC, abstractmethod


class DiggingStrategy(ABC):

    @abstractmethod
    def dig_data(self, **digging_parameters) -> dict:
        pass
