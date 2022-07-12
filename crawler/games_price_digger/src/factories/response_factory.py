import requests


class ChunkedResponseFactory:

    def make_response(self, url):
        return requests.get(url, stream=True)
