# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import csv
from .items import BondItem

class BondPipeline:
    
    def open_spider(self, spider):
        input_file = os.path.join(os.path.dirname(__file__), "../../input/bond_input.csv")
        if os.path.exists(input_file):
            with open(input_file, newline="") as f:
                reader = csv.reader(f)
                spider.set_symbols([row[0] for row in reader])
        else:
            raise AttributeError("No symbols provided.")

        output_file = os.path.join(os.path.dirname(__file__), "../../output/bond_output.csv")
        self.file = open(output_file, 'w', newline="")
        self.writer = csv.DictWriter(self.file, fieldnames=[field for field in BondItem.fields])
        self.writer.writeheader()
        
    def process_item(self, item, spider):
        self.writer.writerow(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        self.file.close()
