import shutil
import requests
from . import DownloadingStrategy


class DefaultDownloading(DownloadingStrategy):
    _response = None

    def download(self, url: str, destination: str) -> None:
        self._response = requests.get(url, stream=True)

        if self._response.status_code == 200:
            self._download_image(destination)

        del self._response

    def _download_image(self, destination):
        with open(destination, 'wb') as image:
            self._response.raw.decode_content = True
            shutil.copyfileobj(self._response.raw, image)
