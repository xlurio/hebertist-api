from abc import ABC, abstractmethod


class ExtractionStrategy(ABC):

    @abstractmethod
    def extract_data(self, game_box_list):
        pass
