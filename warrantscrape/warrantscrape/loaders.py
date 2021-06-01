from scrapy.loader import ItemLoader
from .items import WarrantItem
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class WarrantLoader(ItemLoader):
    default_item_class = WarrantItem
    default_output_processor = TakeFirst()
    