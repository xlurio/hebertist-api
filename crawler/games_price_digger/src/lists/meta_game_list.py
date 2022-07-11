from games_price_digger.src.components.meta_game import MetaGame
from games_price_digger.src.iterators.iterator import Iterator
from games_price_digger.src.iterators.simple_iterator import SimpleIterator
from . import List


class MetaGameList(List):
    _list = []

    def __init__(self, *game_list):
        self._list = [self._validate_item(item) for item in game_list]

    def _validate_item(self, item):
        if isinstance(item, MetaGame):
            return item

        raise TypeError(
            'Item passed is not an instance from games_price_digger.src'
            '.components.meta_game.MetaGame'
        )

    def make_iterator(self) -> Iterator:
        return SimpleIterator(self._list)

    def get_item_at(self, index):
        return self._list[index]

    def add_item(self, item):
        validated_item = self._validate_item(item)
        self._list.append(validated_item)

    def cleanup(self):
        self._list = []
