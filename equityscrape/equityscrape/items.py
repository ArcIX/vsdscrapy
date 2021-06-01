# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy.item import Field

class EquityItem(Item):
    issuer = Field()
    name = Field()
    code = Field()
    isin = Field()
    sec_type = Field()
    par_val = Field()
    market = Field()
    no_of_reg_cert = Field()
    val_of_cur_reg = Field()
    qty_of_cur_reg = Field()
    issuer_method = Field()
    admin_place = Field()
    source_url = Field()
