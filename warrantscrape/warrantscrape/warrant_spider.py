from scrapy import Spider
from scrapy.http import Request

class WarrantSpider(Spider):
    name = "Warrant"
    url = "https://vsd.vn/en/search?text="

    def search_symbols(self):
        for symbol in self.symbols:
            yield Request(self.url + symbol, dont_filter=True, callback=None)

    def get_detail_page_url(self, symbol, response):
        return response.xpath("//*[@id='divGlSearchIsuStocks']//li//b/" + symbol)

    def start_requests(self):
        symbol_requests = self.search_symbols()
        for symbol_request in symbol_requests:
            pass
        
    def set_symbols(self, symbols):
        """
        Give the symbols of the securities to be scraped
        """
        self.search = symbols