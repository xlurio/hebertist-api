from abc import ABC, abstractmethod


class PageGettingStrategy(ABC):

    @abstractmethod
    def get_page(self, url):
        pass
