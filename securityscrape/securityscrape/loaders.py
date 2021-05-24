from scrapy.loader import ItemLoader
from .items import SecurityItem
from scrapy.loader.processors import TakeFirst

class SecurityLoader(ItemLoader):
    default_item_class = SecurityItem
    default_output_processor = TakeFirst()