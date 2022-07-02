from abc import ABC, abstractmethod


class FakeResponseBuilder(ABC):

    @abstractmethod
    def build(self):
        pass
