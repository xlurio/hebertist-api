from scrapy.http import Request, HtmlResponse, Response
from . import FakeResponseBuilder


class HTMLResponseBuilder(FakeResponseBuilder):

    _fake_url = 'http://fakeurl.com/'

    def set_html_file_path(self, html_file_path: str):
        self._html_file_path = html_file_path
        return self

    def build(self) -> Response:
        request = Request(self._fake_url)
        with open(self._html_file_path) as html_file:
            response_body = html_file.read()
        response = HtmlResponse(
            url=self._fake_url,
            request=request,
            body=response_body,
            encoding='utf-8'
        )
        return response
