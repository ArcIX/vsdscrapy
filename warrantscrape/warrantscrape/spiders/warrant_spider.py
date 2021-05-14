from scrapy import Spider, Field
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ..items import WarrantItem
from scrapy.loader.processors import TakeFirst

class WarrantSpider(Spider):
    name = "warrant"
    base_url = "https://vsd.vn"
    search_url = base_url + "/en/search?text="

    def set_symbols(self, symbols):
        """
        Provide the symbols of the securities to be scraped
        """
        self.symbols = symbols

    def start_requests(self):
        """
        On this page: https://vsd.vn/en/search?text=, make a request to search for each symbol
        """
        self.set_symbols([
            "CROS2001",
            "CROS2002"
        ])
        search_urls = [self.search_url + symbol for symbol in self.symbols]
        for index, url in enumerate(search_urls):
            yield Request(url, dont_filter=True, 
                meta={
                    'symbol': self.symbols[index],
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301, 302],
                },
                callback=self.get_detail_page_url
            )

    def get_detail_page_url(self, response):
        """
        Upon searching the symbol, get the url to
        its details page
        """
        symbol = response.meta.get('symbol')
        href = response.xpath(
            """
            //div[@id='divGlSearchIsuStocks']//li//b[text()='{}']/../@href
            """.format(symbol)
        ).get()
        yield Request(self.base_url + href, dont_filter=True,
            meta = {
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302]
            }
        )

    def parse(self, response):
        """
        From the details page of a symbol, get all information for that security
        """
        rows = response.xpath(
            """
            //div[@id='Detail_TCPH_TTCK']/div[@class='news-issuers']/div[@class='row']
            """
        )[:-1]
        warrantItem = WarrantItem()
        warrantLoader = ItemLoader(item=warrantItem, response=response)
        for row in rows:
            key = row.xpath("./div[1]/text()").get()
            key = key.replace(":", "")
            warrantItem.fields[key] = Field(output_processor=TakeFirst())

            value = row.xpath("./div[2]/descendant-or-self::*[last()]/text()").get()
            warrantLoader.add_value(key, value)
        return warrantLoader.load_item()
            