import scrapy

from newsscraper.items import NewsItem
from newsscraper.utils.cleaners import cleanhtml_shorten
from newsscraper.utils.date_parsers import (
    get_current_datetime_eng_custom,
    get_custom_dates,
)
from newsscraper.utils.definitions import BIZPATI


class BizpatiSpider(scrapy.Spider):
    name = "bizpati"
    # allowed_domains = ["bizpati.com"]
    start_urls = ["https://bizpati.com/others-news-stock-market"]

    def parse(self, response):
        news = response.css(
            "div.category_wrapper div.container-fluid a::attr(href)"
        ).extract()

        for url in news:
            yield response.follow(url, callback=self.parse_news_detail)

    def parse_news_detail(self, response):
        news_item = NewsItem()

        news_item["source"] = "Bizpati"

        # urls
        if response.xpath("//meta[contains(@property, 'og:title')]"):
            news_item["image_url"] = response.xpath(
                "//meta[contains(@property, 'og:image')]/@content"
            ).get()
        news_item["url"] = response.url

        # titles
        news_item["headline"] = response.xpath(
            "//meta[contains(@property, 'og:title')]/@content"
        ).get()
        news_item["subtitle"] = cleanhtml_shorten(
            response.css("div.article-container p").get()
        )

        # dates
        date_str = get_custom_dates(
            response.xpath("//figcaption/p[2]/span/text()").get(), BIZPATI
        )
        news_item["date"] = date_str["eng"]
        news_item["nepdate"] = date_str["nep"]
        news_item["scraped_datetime"] = get_current_datetime_eng_custom()

        news_item["scrip"] = []

        yield news_item
