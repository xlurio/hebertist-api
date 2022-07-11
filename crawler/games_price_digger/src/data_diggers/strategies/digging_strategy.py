from abc import ABC, abstractmethod
from games_price_digger.src.builders.digging_settings_builder import DiggingSettingsBuilder


class DiggingStrategy(ABC):

    @abstractmethod
    def make_settings_builder(self, *args, **kwargs) -> DiggingSettingsBuilder:
        pass

    @abstractmethod
    def dig_data(self, settings) -> dict:
        pass
