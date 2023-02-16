import scrapy


class NepalstockSpider(scrapy.Spider):
    name = 'nepalstock'
    allowed_domains = ['nepalstock.com']
    start_urls = ['http://nepalstock.com/']

    def parse(self, response):
        pass
