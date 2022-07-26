import django
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from games_price_digger import spiders

django.setup()


class PriceCrawler():
    """Crawls the game prices"""
    data_name = 'Prices'

    spiders = (
        spiders.SteamPriceSpider,
        spiders.GogPriceSpider,
        spiders.GreenManPriceSpider,
    )

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()

    def run_crawler(self):
        process = CrawlerProcess(self.settings)

        for spider in self.spiders:
            process.crawl(spider)

        process.start()


if __name__ == '__main__':
    crawler = PriceCrawler()
    crawler.run_crawler()
