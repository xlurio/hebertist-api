from abc import ABC, abstractmethod


class FakeModel(ABC):
    @abstractmethod
    def save(self, commit) -> None:
        pass
