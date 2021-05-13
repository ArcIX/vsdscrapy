from scrapy import Spider
from scrapy.http import Request

class WarrantSpider(Spider):
    name = "warrant"
    base_url = "https://vsd.vn"
    search_url = base_url + "/en/search?text="

    def start_requests(self):
        self.set_symbols(
            [
                "CROS2001",
                "CROS2002"
            ]
        )
        for index, url in enumerate(self.start_urls):
            yield Request(url, dont_filter=True, meta = {
                'symbol': self.symbols[index],
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302],
            }, callback=self.get_detail_page_url)

    def set_symbols(self, symbols):
        """
        Provide the symbols of the securities to be scraped
        """
        self.symbols = symbols
        self.start_urls = [self.search_url + symbol for symbol in self.symbols]

    def search_symbols(self):
        """
        On this page: https://vsd.vn/en/search?text=, make a request to search for each symbol
        """
        for symbol in self.symbols:
            yield Request(self.search_url + symbol, callback=self.get_detail_page_url, meta={'symbol': symbol})
        else:
            raise AttributeError("Symbols to search not provided using set_symbols")

    def get_detail_page_url(self, response):
        """
        Upon searching the symbol, get the url to
        its details page
        """
        symbol = response.meta.get('symbol')
        href = response.xpath("//div[@id='divGlSearchIsuStocks']//li//b[text()='" + symbol + "']/../@href").get()
        yield Request(self.base_url + href, dont_filter=True, meta = {
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302],
        })

    def parse(self, response):
        """
        From the details page of a symbol, get all information for that security
        """
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        security = {}
        rows = response.xpath("//div[@id='Detail_TCPH_TTCK']/div[@class='news-issuers']/div[@class='row']")[:-1]
        for row in rows:
            key = row.xpath("./div[1]/text()").get()
            key = key.replace(":", "")
            value = row.xpath("./div[2]/descendant-or-self::*[last()]/text()").get()
            security[key] = value
        return security
            