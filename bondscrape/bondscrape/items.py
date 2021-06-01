# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy.item import Field

class BondItem(Item):
    issuer = Field()
    name = Field()
    code = Field()
    isin = Field()
    sec_type = Field()
    par_val = Field()
    market = Field()
    no_of_reg_cert = Field()
    no_of_cur_reg = Field()
    val_of_cur_reg = Field()
    qty_of_cur_reg = Field()
    issuer_method = Field()
    int_rate = Field()
    pay_method =Field()
    term = Field()
    release_date = Field()
    due_date =Field()
    admin_place = Field()
    source_url = Field()