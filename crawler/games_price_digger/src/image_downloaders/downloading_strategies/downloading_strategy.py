from abc import ABC, abstractmethod


class DownloadingStrategy(ABC):

    @abstractmethod
    def download(self, url: str, destination: str) -> None:
        pass
