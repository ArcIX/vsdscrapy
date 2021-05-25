from scrapy import Spider
from scrapy.http import Request
from ..loaders import WarrantLoader
import os
import csv

class WarrantSpider(Spider):
    name = "warrant"
    base_url = "https://vsd.vn"
    search_url = base_url + "/en/search?text="

    def set_symbols(self, symbols):
        """
        Provide the symbols of the securities to be scraped.
        DO NOT USE THIS IF SYMBOLS WILL BE PROVIDED VIA CSV
        """
        self.symbols = symbols

    def start_requests(self):
        """
        On this page: https://vsd.vn/en/search?text=, make a request to search for each symbol
        """
        # Sample symbols to scrape
        # self.set_symbols([
        #     "CROS2001",
        #     "CROS2002"
        # ])
        input_file = os.path.join(os.path.dirname(__file__), "../../../input/inputsymbols.csv")
        if not hasattr(self, 'symbols') and os.path.exists(input_file):
            with open(input_file, newline="") as f:
                reader = csv.reader(f)
                self.symbols = [row[0] for row in reader]
                print(self.symbols)
        else:
            raise AttributeError("No symbols provided.")
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
        warrantLoader = WarrantLoader(
            selector = """
            //div[@id='Detail_TCPH_TTCK']/div[@class='news-issuers']
            """
        )
        xpaths = {
            'issuer' : "./div[text()=\"Issuer's name:\"]/following-sibling::node()/a/text()",
            'name' : "./div[text()='Name of warrant:']/following-sibling::node()/text()",
            'code' : "./div[text()='Warrant code:']/following-sibling::node()/text()",
            'isin' : "./div[text()='ISINs:']/following-sibling::node()/text()",
            'underlying' : "./div[text()='Underlying securities:']/following-sibling::node()/text()",
            'ul_issuer' : "./div[text()='Issuer of underlying securities:']/following-sibling::node()/text()",
            'wrt_type' : "./div[text()='Warrant type:']/following-sibling::node()/text()",
            'exer_style' : "./div[text()='Exercise style:']/following-sibling::node()/text()",
            'settle_method' : "./div[text()='Settlement method:']/following-sibling::node()/text()",
            'term' : "./div[text()='Term:']/following-sibling::node()/text()",
            'due_date' : "./div[text()='Due date:']/following-sibling::node()/text()",
            'conv_ratio' : "./div[text()='Conversion ratio:']/following-sibling::node()/text()",
            'strike_price' : "./div[text()='Strike price:']/following-sibling::node()/text()",
            'issue_price' : "./div[text()='Initial issuance price:']/following-sibling::node()/text()",
            'market' : "./div[text()='Trading market:']/following-sibling::node()/text()",
            'no_of_reg_cert' : "./div[text()='Number of Covered warrant Registration Certificate:']/following-sibling::node()/text()",
            'no_of_init_reg' : "./div[text()='Number of initially registered covered warrants at VSD:']/following-sibling::node()/text()",
            'val_of_init_reg' : "./div[text()='The value of initially registered covered warrant basing on the issuance price at VSD:']/following-sibling::node()/text()",
            'qty_of_init_reg' : "./div[text()='Quantity of registered covered warrants at VSD:']/following-sibling::node()/text()",
            'issuer_method' : "./div[text()='Issuer method:']/following-sibling::node()/text()",
            'admin_place' : "./div[text()='Administration Place:']/following-sibling::node()/text()"
        }
        for key, value in xpaths:
            warrantLoader.add_xpath(key, value)
        warrantLoader.add_value('source_url', response.request.url)
        return warrantLoader.load_item()