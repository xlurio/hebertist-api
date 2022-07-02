from abc import ABC, abstractmethod
from games_price_digger.src.lists.game_box_list import GameBoxList

from games_price_digger.src.lists.game_list import GameList


class ExtractionStrategy(ABC):

    @abstractmethod
    def extract_data(self, game_box_list: GameBoxList) -> GameList:
        pass
