import os

from games_price_digger.src.image_downloaders.downloading_strategies.default_downloading import DefaultDownloading
from games_price_digger.src.image_downloaders.downloading_strategies.downloading_strategy import DownloadingStrategy
from games_price_digger.src.image_downloaders.naming_strategies.naming_strategy import NamingStrategy
from games_price_digger.src.image_downloaders.naming_strategies.uud4_naming import UUD4Naming


class ImageDownloader:
    _filename = ''

    def __init__(self,
                 destination_folder,
                 downloading_strategy: DownloadingStrategy =
                 DefaultDownloading(),
                 naming_strategy: NamingStrategy = UUD4Naming()):
        self._destination_folder = destination_folder
        self._downloading_strategy = downloading_strategy
        self._naming_strategy = naming_strategy

    def download(self, url):
        extension = str(url).split('.')[-1]

        self._filename = self._naming_strategy.get_filename(extension)
        destination = os.path.join(
            self._destination_folder,
            self._filename
        )

        self._downloading_strategy.download(
            url, destination
        )

    def get_filename(self):
        return self._filename
