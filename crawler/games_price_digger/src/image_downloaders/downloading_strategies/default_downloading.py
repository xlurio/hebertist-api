import shutil

from games_price_digger.src.factories.response_factory import \
    ChunkedResponseFactory
from . import DownloadingStrategy


class DefaultDownloading(DownloadingStrategy):
    _response = None
    _response_factory = ChunkedResponseFactory()

    def download(self, url: str, destination: str) -> None:
        self._response = self._response_factory.make_response(url)

        if self._response.status_code == 200:
            self._download_image(destination)

        del self._response

    def _download_image(self, destination):
        with open(destination, 'wb') as image:
            self._decode_content()
            shutil.copyfileobj(self._response.raw, image)

    def _decode_content(self):
        try:
            self._response.raw.decode_content = True
        except AttributeError:
            pass
