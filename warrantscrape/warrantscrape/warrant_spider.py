from scrapy import Spider
from scrapy.http import Request

class WarrantSpider(Spider):
    name = "Warrant"
    base_url = "https://vsd.vn"
    search_url = base_url + "/en/search?text="

    def set_symbols(self, symbols):
        """
        Provide the symbols of the securities to be scraped
        """
        self.search = symbols

    def search_symbols(self):
        """
        On this page: https://vsd.vn/en/search?text=, make a request to search for each symbol
        """
        for symbol in self.symbols:
            yield Request(self.search_url + symbol, callback=self.get_detail_page_url, meta={'symbol': symbol})
        else:
            raise ValueError("Symbols to search not provided using set_symbols")

    def get_detail_page_url(self, response):
        """
        Upon searching the symbol, get the url to
        its details page
        """
        symbol = response.meta.get('symbol')
        return response.xpath("//*[@id='divGlSearchIsuStocks']//li//b[text()='" + symbol + "']/../@href")

    def start_requests(self):
        """
        After getting a list of all urls to each symbol's details page, make a request to each of them
        """
        detail_page_urls = self.search_symbols()
        for detail_page_url in detail_page_urls:
            yield Request(detail_page_url, dont_filter=True)

    def parse(self, response):
        """
        From the details page of a symbol, get all information for that security
        """
        for row in response.xpath("//div[@id='Detail_TCPH_TTCK']/div[@class='news-issuers']/div[@class='row']"):
            key = row.xpath("./div[1]/text()").get()
            key = key.replace(":", "")
            value = row.xpath("./div[2]/descendant-or-self::*[last()]/text()").get()
            yield {key: value}