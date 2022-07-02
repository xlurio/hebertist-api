from games_price_digger.src.components import FoundGame
from games_price_digger.src.components.search import Search
from . import GameList


class SearchGameList(GameList):

    _list = []

    def __init__(self, search: Search):
        self._search = search

    def add_item(self, item: FoundGame) -> None:
        game_name = item.get_name()
        if self._search.is_the_searched_game(game_name):
            return super().add_item(item)
