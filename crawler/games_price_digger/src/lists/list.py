from abc import ABC, abstractmethod
from games_price_digger.src.iterators import Iterator


class List(ABC):

    @abstractmethod
    def make_iterator(self) -> Iterator:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass
