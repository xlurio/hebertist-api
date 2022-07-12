from games_price_digger.src.utils.fake_response_builders.html_response_builder import HTMLResponseBuilder
from games_price_digger.src.utils.test_html_getter import TestHTMLGetter
from scrapy.http import Response


class FakeResponseFactory:

    def make_response(self, page_source_file: str) -> Response:
        html_getter = TestHTMLGetter()
        html_path = html_getter.get_html_file_by_name(page_source_file)

        fake_response_builder = HTMLResponseBuilder()
        fake_response_builder.set_html_file_path(html_path)
        return fake_response_builder.build()
