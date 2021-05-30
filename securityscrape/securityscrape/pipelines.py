# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import csv
import json

class SecurityPipeline:
    
    def open_spider(self, spider):
        # Get symbols from csv file in input folder
        input_file = os.path.join(os.path.dirname(__file__), "../../input/inputsymbols.csv")
        if os.path.exists(input_file):
            with open(input_file, newline="") as f:
                reader = csv.reader(f)
                spider.symbols = [row[0] for row in reader]
        else:
            raise AttributeError("No symbols provided.")

        # Set the processors per field
        # spider.processors = {
        #     'the_value_of_currently_registered_securities': {
        #         'in': lambda vals: [val.replace(" ", "").replace(",", "").replace("VND", "") for val in vals],
        #     },
        #     'issuers_name': {
        #         'in': lambda vals: [val.lower() for val in vals],
        #     },
        #     'trading_market': {
        #         'in': lambda vals: [val.lower() for val in vals],
        #     }
        # }

        # Open json file in output folder; Create if not existing
        output_file = os.path.join(os.path.dirname(__file__), "../../output/outputsymbols.json")
        self.file = open(output_file, 'w')

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
