from abc import ABC, abstractmethod

from scrapy import Selector


class DiggingSettingsBuilder(ABC):

    @abstractmethod
    def set_item_box(self, box: Selector):
        pass
