from scrapy.loader import ItemLoader
from .items import EquityItem
from itemloaders.processors import TakeFirst, MapCompose

def strip_vnd_to_int(text):
    return int(text.replace(" VND", "").replace(",", ""))

def strip_sec_to_int(text):
    return int(text.replace(" Securites", "").replace(",", ""))

class EquityLoader(ItemLoader):
    default_item_class = EquityItem
    default_output_processor = TakeFirst()

    par_val_in = MapCompose(strip_vnd_to_int)
    qty_of_cur_reg_in = MapCompose(strip_sec_to_int)
    val_of_cur_reg_in = MapCompose(strip_vnd_to_int)