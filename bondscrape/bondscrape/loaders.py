from scrapy.loader import ItemLoader
from .items import BondItem
from itemloaders.processors import TakeFirst

class BondLoader(ItemLoader):
    default_item_class = BondItem
    default_output_processor = TakeFirst()