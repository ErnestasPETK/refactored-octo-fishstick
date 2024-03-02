# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .db import get_session


class AruodasPipeline:

    def __init__(self):
        self.logger = logging.getLogger("AruodasPipeline")
        self.session = None

    async def open_spider(self, spider):
        self.logger.info("Opening spider")
        self.session = get_session()

    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        logging.info("Processing pipeline item")
        logging.info(f"item: {item}")

        return item
