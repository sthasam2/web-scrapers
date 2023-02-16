from datetime import datetime

import scrapy

from newsscraper.items import NewsItem
from newsscraper.utils.date_parsers import (
    get_current_datetime_eng_custom,
    get_custom_dates,
)
from newsscraper.utils.definitions import NEPALIPAISA


class NepalipaisaMarketNewsSpider(scrapy.Spider):
    name = "nepalipaisa"
    allowed_domains = ["nepalipaisa.com"]
    start_urls = ["http://www.nepalipaisa.com/Stock-Market.aspx"]

    def parse(self, response):
        links = response.css(".Shareli h2 a::attr(href)").extract()

        for link in links:
            yield response.follow(link, callback=self.news_detail_parse)

    def news_detail_parse(self, response):
        news_item = NewsItem()

        news_item["source"] = "Nepalipaisa"

        # urls
        news_item["image_url"] = (
            response.xpath("//meta[20]").css("::attr(content)").get()
        )
        news_item["url"] = response.xpath("//meta[21]").css("::attr(content)").get()

        # titles
        news_item["headline"] = (
            response.xpath("//meta[18]").css("::attr(content)").get()
        )
        news_item["subtitle"] = (
            response.css("meta#MetaDescription ::attr(content)").get()[:200] + "..."
        )

        # dates
        date_str = get_custom_dates(
            response.xpath("//meta[22]").css("::attr(content)").get(), NEPALIPAISA
        )
        news_item["date"] = date_str["eng"]
        news_item["nepdate"] = date_str["nep"]
        news_item["scraped_datetime"] = get_current_datetime_eng_custom()

        news_item["scrip"] = []

        yield news_item
