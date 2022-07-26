import django

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

django.setup()

try:
    from games_price_digger.spiders.games_metascore import GamesMetascoreSpider
except ImportError:
    raise ImportError("Web API not setted")


class GameCrawler():
    """Crawls the game and score"""
    data_name = 'Games'

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()

    def run_crawler(self):
        process = CrawlerProcess(self.settings)
        process.crawl(GamesMetascoreSpider)
        process.start()


if __name__ == '__main__':
    crawler = GameCrawler()
    crawler.run_crawler()
