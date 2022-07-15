from games_price_digger.src.data_getters.strategies.extraction_strategy \
    import ExtractionStrategy
from games_price_digger.src.lists.game_box_list import GameBoxList
from games_price_digger.src.lists.game_list import GameList


class PageDataExtractor:

    def __init__(self, strategy: ExtractionStrategy) -> None:
        self._strategy = strategy

    def extract_data(self, game_box_list: GameBoxList) -> GameList:
        return self._strategy.extract_data(game_box_list)
