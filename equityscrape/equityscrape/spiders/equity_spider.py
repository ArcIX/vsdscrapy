import sys
sys.path.append("..")

from securityscrape.securityscrape.spiders.security_spider import SecuritySpider
from ..loaders import EquityLoader

class EquitySpider(SecuritySpider):
    name = "equity"
    xpaths = {
        'issuer' : "//div[text()=\"Issuer's name:\"]/following-sibling::node()/a/text()",
        'name' : "//div[text()='Securities name:']/following-sibling::node()/text()",
        'code' : "//div[text()='Securities code:']/following-sibling::node()/text()",
        'isin' : "//div[text()='ISINs:']/following-sibling::node()/text()",
        'sec_type' : "//div[text()='Securities type:']/following-sibling::node()/text()",
        'par_val' : "//div[text()='Par value:']/following-sibling::node()/text()",
        'market' : "//div[text()='Trading market ']/following-sibling::node()/text()",
        'no_of_reg_cert' : "//div[text()='Number of Securities Registration Certificate:']/following-sibling::node()/text()",
        'val_of_cur_reg' : "//div[text()='The value of currently registered securities:']/following-sibling::node()/text()",
        'qty_of_cur_reg' : "//div[text()='Quantity of currently registered securities:']/following-sibling::node()/text()",
        'issuer_method' : "//div[text()='Issuer method:']/following-sibling::node()/text()",
        'admin_place' : "//div[text()='Administration Place:']/following-sibling::node()/text()"
    }

    def parse(self, response):
        """
        From the details page of a symbol, get all information for that security
        """
        equityLoader = EquityLoader(response=response)
        if hasattr(self, 'processors'):
            for key in self.processors:
                if 'in' in self.processors[key]:
                    setattr(equityLoader, key + "_in", self.processors[key]['in'])
                if 'out' in self.processors[key]:
                    setattr(equityLoader, key + "_out", self.processors[key]['out'])
        for key in self.xpaths:
            equityLoader.add_xpath(key, self.xpaths[key])
        equityLoader.add_value('source_url', response.request.url)
        return equityLoader.load_item()