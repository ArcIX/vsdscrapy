from typing import Type
from scrapy import Spider, Field
from scrapy.http import Request
from ..loaders import SecurityLoader
from ..items import SecurityItem

class SecuritySpider(Spider):
    name = "security"
    _base_url = "https://vsd.vn"
    _search_url = _base_url + "/en/search?text="

    @property
    def symbols(self):
        return self._symbols

    @symbols.setter
    def symbols(self, symbols):
        if not isinstance(symbols, list):
            raise TypeError("Symbols are not in a list.")
        self._symbols = symbols

    @property
    def processors(self):
        return self._processors

    @processors.setter
    def processors(self, processors):
        if not isinstance(processors, dict):
            raise TypeError("Processors are expected as dictionary.")
        self._processors = processors

    def start_requests(self):
        """
        On this page: https://vsd.vn/en/search?text=, make a request to search for each symbol
        """
        print(self.symbols)
        search_urls = [self._search_url + symbol for symbol in self.symbols]
        for index, url in enumerate(search_urls):
            yield Request(url, dont_filter=True, 
                meta={
                    'symbol': self.symbols[index],
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301, 302],
                },
                callback=self._get_detail_page_url
            )

    def _get_detail_page_url(self, response):
        """
        Upon searching the symbol, get the url to
        its details page and make a request to view it
        """
        symbol = response.meta.get('symbol')
        href = response.xpath(
            """
            //div[@id='divGlSearchIsuStocks']//li//b[text()='{}'
            and starts-with(following-sibling::text(), ':')
            and not(preceding-sibling::text())]/../@href
            """.format(symbol)
        ).get()
        yield Request(self._base_url + href, dont_filter=True,
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
        securityItem = SecurityItem()
        securityLoader = SecurityLoader(item=securityItem)
        for row in rows:
            key = row.xpath("./div[1]/text()").get()
            key = key.replace(":", "").replace("'", "").strip().replace(" ", "_").lower()
            securityItem.fields[key] = Field()

            value = row.xpath("./div[2]/descendant-or-self::*[last()]/text()").get()

            if hasattr(self, '_processors'):
                if key in self._processors:
                    if 'in' in self._processors[key]:
                        setattr(securityLoader, key + "_in", self.processors[key]['in'])
                    if 'out' in self._processors[key]:
                        setattr(securityLoader, key + "_out", self.processors[key]['out'])
            
            securityLoader.add_value(key, value)
        securityLoader.add_value('source_url', response.request.url)
        return securityLoader.load_item()