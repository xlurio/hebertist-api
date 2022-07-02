from abc import ABC, abstractmethod


class DriveFactory(ABC):

    @abstractmethod
    def make_driver(self, **kwargs):
        pass
