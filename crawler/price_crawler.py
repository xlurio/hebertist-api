from games_price_digger import spiders
import base_crawler
import django
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

django.setup()


class PriceCrawler(base_crawler.Crawler):
    """Crawls the game prices"""
    data_name = 'Prices'

    spiders = (
        spiders.steam_price.SteamPriceSpider,
        spiders.gog_price.GogPriceSpider,
        spiders.greenman_price.GreenManPriceSpider,
    )

    def __init__(self, ):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        settings = get_project_settings()
        runner = CrawlerRunner(settings)

        for spider in self.spiders:
            runner.crawl(spider)

        d = runner.join()
        d.addBoth(lambda _: reactor.stop())


if __name__ == '__main__':
    crawler = PriceCrawler()
    crawler.run_crawler()
