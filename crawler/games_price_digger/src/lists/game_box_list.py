from games_price_digger.src.iterators.iterator import Iterator
from games_price_digger.src.iterators.simple_iterator import SimpleIterator
from games_price_digger.src.lists.list import List
from scrapy import Selector


class GameBoxList(List):

    def __init__(self, *boxes):
        self._list = [self._validate_box(box) for box in boxes]

    def _validate_box(self, box):
        if isinstance(box, Selector):
            return box

        raise TypeError(
            'Item passed is not an instance from scrapy.selector.Selector'
        )

    def make_iterator(self) -> Iterator:
        return SimpleIterator(self._list)

    def get_item_at(self, index) -> Selector:
        return self._list[index]

    def cleanup(self) -> None:
        self._list = []
