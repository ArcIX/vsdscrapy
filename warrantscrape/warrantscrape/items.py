# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class WarrantItem(Item):
    issuer = Field()
    name = Field()
    code = Field()
    isin = Field()
    underlying = Field()
    ul_issuer = Field()
    wrt_type = Field()
    exer_style = Field()
    settle_method = Field()
    term = Field()
    due_date = Field()
    conv_ratio = Field()
    strike_price = Field()
    issue_price = Field()
    market = Field()
    no_of_reg_cert = Field()
    no_of_init_reg = Field()
    val_of_init_reg = Field()
    qty_of_init_reg = Field()
    issuer_method = Field()
    admin_place = Field()
    source_url = Field()