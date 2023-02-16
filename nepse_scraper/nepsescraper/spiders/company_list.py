import scrapy
import json
from humps import decamelize

from nepsescraper.items import CompanyListItem


class CompanyListSpider(scrapy.Spider):
    name = "company_list"
    start_urls = ["https://newweb.nepalstock.com/api/nots/company/list/"]

    def parse(self, response):
        raw_data = json.loads(response.body)

        item = CompanyListItem()
        for data in raw_data:
            for key, value in data.items():
                snake_key = decamelize(key)
                item[snake_key] = value
            yield item
