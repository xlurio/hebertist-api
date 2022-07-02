from games_price_digger.src.components import Game
from games_price_digger.src.iterators.iterator import Iterator
from games_price_digger.src.iterators.simple_iterator import SimpleIterator
from . import List


class GameList(List):
    def __init__(self, *games):
        self._list = [
            self._validate_game(game) for game in games
        ]

    def _validate_game(self, game) -> Game:
        is_a_game = isinstance(game, Game)
        if is_a_game:
            return game
        raise TypeError('A non game object was passed')

    def make_iterator(self) -> Iterator:
        return SimpleIterator(self._list)

    def get_item_at(self, index) -> Game:
        return self._list[index]

    def add_item(self, item) -> None:
        game = self._validate_game(item)
        self._list.append(game)

    def cleanup(self) -> None:
        self._list = []

    def __eq__(self, __o: object) -> bool:
        sorted_list = self._list.sort()
        sorted_other_list = __o._list.sort()
        return sorted_list == sorted_other_list
