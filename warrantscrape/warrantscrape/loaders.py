from scrapy.loader import ItemLoader
from .items import WarrantItem
from scrapy.loader.processors import TakeFirst, MapCompose
from datetime import datetime as dt

def strip_months_to_int(text):
    return int(text.replace(" months", ""))

def reformat_date(date):
    return dt.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

def ratio_to_decimal(ratio):
    x, y = ratio.split(":")
    x = int(x.replace(",", ""))
    y = int(y.replace(",", ""))
    return x / y

def strip_vnd_to_int(text):
    return int(text.replace(" VND", "").replace(",", ""))

def strip_vnd_per_wrt_to_int(text):
    return int(text.replace(" VND/covered warrant", "").replace(",", ""))

def strip_cov_wrt_to_int(text):
    return int(text.replace(" Covered warrant", "").replace(" covered warrant", "").replace(",", ""))

class WarrantLoader(ItemLoader):
    default_item_class = WarrantItem
    default_output_processor = TakeFirst()

    term_in = MapCompose(strip_months_to_int)
    due_date_in = MapCompose(reformat_date)
    conv_ratio_in = MapCompose(ratio_to_decimal)
    strike_price_in = MapCompose(strip_vnd_to_int)
    issue_price_in = MapCompose(strip_vnd_per_wrt_to_int)
    no_of_init_reg_in =  MapCompose(strip_cov_wrt_to_int)
    val_of_init_reg_in = MapCompose(strip_vnd_to_int)
    qty_of_init_reg_in = MapCompose(strip_cov_wrt_to_int)