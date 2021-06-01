from scrapy.loader import ItemLoader
from .items import EquityItem
from itemloaders.processors import TakeFirst

class EquityLoader(ItemLoader):
    default_item_class = EquityItem
    default_output_processor = TakeFirst()