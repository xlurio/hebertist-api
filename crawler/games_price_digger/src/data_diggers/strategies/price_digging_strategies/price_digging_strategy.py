from abc import ABC, abstractmethod


class PriceDiggingStrategy(ABC):

    @abstractmethod
    def dig_data(self, element):
        pass
