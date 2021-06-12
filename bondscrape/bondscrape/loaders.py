from scrapy.loader import ItemLoader
from .items import BondItem
from itemloaders.processors import TakeFirst, MapCompose
from datetime import datetime as dt

def strip_vnd_to_int(text):
    return int(text.replace(" VND", "").replace(",", ""))

def strip_bond_to_int(text):
    return int(text.replace(" Bond", "").replace(",", ""))

def strip_years_to_int(text):
    return int(text.replace(" years", ""))

def reformat_date(date):
    return dt.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

class BondLoader(ItemLoader):
    default_item_class = BondItem
    default_output_processor = TakeFirst()

    par_val_in = MapCompose(strip_vnd_to_int)
    qty_of_cur_reg_in = MapCompose(strip_bond_to_int)
    val_of_cur_reg_in = MapCompose(strip_vnd_to_int)
    term_in = MapCompose(strip_years_to_int)
    release_date_in = MapCompose(reformat_date)
    due_date_in = MapCompose(reformat_date)