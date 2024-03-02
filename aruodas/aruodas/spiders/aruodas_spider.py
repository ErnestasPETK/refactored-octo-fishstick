from pathlib import Path

import scrapy
from scrapy.http import Response

from ..items import AruodasPageItem


class AruodasSpider(scrapy.Spider):
    name = "aruodas_spider"

    def start_requests(self):
        urls = [
            "https://www.aruodas.lt/",
            # "https://www.aruodas.lt/butai/vilniuje/",
            # "https://www.aruodas.lt/butai/vilniuje/?FRoomNumMin=1&FRoomNumMax=2&FPriceMin=100000&FPriceMax=130000",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response):
        self.logger.info("Received")
        aruodas_page = AruodasPageItem(url=response.url)
        self.logger.info(f"Page item ->  {aruodas_page}")
        self.logger.info(f"response : {response}")
