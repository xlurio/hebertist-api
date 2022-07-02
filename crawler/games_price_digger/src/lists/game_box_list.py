from games_price_digger.src.iterators.iterator import Iterator
from games_price_digger.src.iterators.simple_iterator import SimpleIterator
from games_price_digger.src.lists.list import List
from scrapy import Selector


class GameBoxList(List):

    def __init__(self, *boxes):
        self._list = [box for box in boxes]

    def make_iterator(self) -> Iterator:
        return SimpleIterator(self._list)

    def get_item_at(self, index) -> Selector:
        return self._list[index]

    def cleanup(self) -> None:
        self._list = []
