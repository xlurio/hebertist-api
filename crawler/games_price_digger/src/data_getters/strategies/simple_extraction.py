from games_price_digger.src.builders.digging_settings_builder import DiggingSettingsBuilder
from games_price_digger.src.components.found_game import FoundGame
from games_price_digger.src.components.search import Search
from games_price_digger.src.data_diggers.data_digger import DataDigger
from games_price_digger.src.lists.game_box_list import GameBoxList
from games_price_digger.src.lists.game_list import GameList
from games_price_digger.src.lists.search_game_list import SearchGameList

from . import ExtractionStrategy


class SimpleExtraction(ExtractionStrategy):

    def __init__(self, digging_settings_builder: DiggingSettingsBuilder,
                 search: Search, data_digger: DataDigger) -> None:
        self._settings_builder = digging_settings_builder
        self._search = search
        self._data_digger = data_digger

    def extract_data(self, game_box_list: GameBoxList) -> GameList:
        list_iteration = game_box_list.make_iterator()
        game_list = SearchGameList(self._search)
        game_list.cleanup()

        while not list_iteration.is_done():
            current_index = list_iteration.get_index()
            current_game_box = game_box_list.get_item_at(current_index)

            self._settings_builder.set_item_box(current_game_box)
            settings = self._settings_builder.build()

            parsed_data = self._data_digger.dig_data(settings)
            game = FoundGame(**parsed_data)
            game_list.add_item(game)

            list_iteration.next()

        return game_list
