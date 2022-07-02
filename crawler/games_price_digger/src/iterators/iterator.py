from abc import ABC, abstractmethod


class Iterator(ABC):

    @abstractmethod
    def first(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def is_done(self):
        pass

    @abstractmethod
    def get_index(self):
        pass
