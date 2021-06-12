import sys
sys.path.append("..")

from securityscrape.securityscrape.spiders.security_spider import SecuritySpider
from ..loaders import WarrantLoader

class WarrantSpider(SecuritySpider):
    name = "warrant"
    xpaths = {
        'issuer' : "//div[text()=\"Issuer's name:\"]/following-sibling::node()/a/text()",
        'name' : "//div[text()='Name of warrant:']/following-sibling::node()/text()",
        'code' : "//div[text()='Warrant code:']/following-sibling::node()/text()",
        'isin' : "//div[text()='ISINs:']/following-sibling::node()/text()",
        'underlying' : "//div[text()='Underlying securities:']/following-sibling::node()/text()",
        'ul_issuer' : "//div[text()='Issuer of underlying securities:']/following-sibling::node()/text()",
        'wrt_type' : "//div[text()='Covered warrant type:']/following-sibling::node()/text()",
        'exer_style' : "//div[text()='Excercise style:']/following-sibling::node()/text()",
        'settle_method' : "//div[text()='Settlement method:']/following-sibling::node()/text()",
        'term' : "//div[text()='Term:']/following-sibling::node()/text()",
        'due_date' : "//div[text()='Due date:']/following-sibling::node()/text()",
        'conv_ratio' : "//div[text()='Conversion ratio:']/following-sibling::node()/text()",
        'strike_price' : "//div[text()='Strike price:']/following-sibling::node()/text()",
        'issue_price' : "//div[text()='Initial issuance price:']/following-sibling::node()/text()",
        'market' : "//div[text()='Trading market:']/following-sibling::node()/text()",
        'no_of_reg_cert' : "//div[text()='Number of Covered warrant Registration Certificate:']/following-sibling::node()/text()",
        'no_of_init_reg' : "//div[text()='Number of initially registered covered warrants at VSD:']/following-sibling::node()/text()",
        'val_of_init_reg' : "//div[text()='The value of initially registered covered warrant basing on the issuance price at VSD:']/following-sibling::node()/text()",
        'qty_of_init_reg' : "//div[text()='Quantity of registered covered warrants at VSD:']/following-sibling::node()/text()",
        'issuer_method' : "//div[text()='Issuer method:']/following-sibling::node()/text()",
        'admin_place' : "//div[text()='Administration Place:']/following-sibling::node()/text()"
    }
    
    def parse(self, response):
        """
        From the details page of a symbol, get all information for that security
        """
        warrantLoader = WarrantLoader(response=response)
        if hasattr(self, 'processors'):
            for key in self.processors:
                if 'in' in self.processors[key]:
                    setattr(warrantLoader, key + "_in", self.processors[key]['in'])
                if 'out' in self.processors[key]:
                    setattr(warrantLoader, key + "_out", self.processors[key]['out'])
        for key in self.xpaths:
            warrantLoader.add_xpath(key, self.xpaths[key])
        warrantLoader.add_value('source_url', response.request.url)
        return warrantLoader.load_item()