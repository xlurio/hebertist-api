from abc import ABC, abstractmethod


class DiggingSettings(ABC):

    @abstractmethod
    def make_item(self, **kwargs):
        pass
