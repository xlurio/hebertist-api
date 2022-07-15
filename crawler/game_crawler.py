import logging
import base_crawler
import django

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

django.setup()

try:
    from games_price_digger.spiders.games_metascore import GamesMetascoreSpider
except ImportError:
    raise ImportError("API not setted")


class GameCrawler(base_crawler.Crawler):
    """Crawls the game and score"""
    data_name = 'Games'

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    d = runner.crawl(GamesMetascoreSpider)


if __name__ == '__main__':
    crawler = GameCrawler()
    crawler.run_crawler()
