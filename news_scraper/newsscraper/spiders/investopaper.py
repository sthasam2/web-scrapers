import scrapy

from newsscraper.items import NewsItem
from newsscraper.utils.cleaners import cleanhtml_shorten
from newsscraper.utils.date_parsers import (
    get_current_datetime_eng_custom,
    get_custom_dates,
)
from newsscraper.utils.definitions import INVESTOPAPER


class InvestopaperSpider(scrapy.Spider):
    name = "investopaper"
    allowed_domains = ["investopaper.com"]
    start_urls = ["http://investopaper.com/articles"]

    page_number = 1
    max_page = 2

    latest_news = None
    links = []

    def parse(self, response):
        page_links = response.css("a.news-more-link::attr(href)").extract()
        InvestopaperSpider.links += page_links

        if InvestopaperSpider.page_number < InvestopaperSpider.max_page:
            InvestopaperSpider.page_number += 1
            next_page = f"https://www.investopaper.com/articles/page/{InvestopaperSpider.page_number}"
            yield response.follow(next_page, callback=self.parse)

        # Executes news detail parsing after link collection is completed
        for link in InvestopaperSpider.links:
            yield response.follow(link, callback=self.news_detail_parse)

        InvestopaperSpider.latest_news = InvestopaperSpider.links[0]

    def news_detail_parse(self, response):
        """
        Get the detailed info from page
        """
        news_item = NewsItem()

        news_item["source"] = "Investopaper"

        # urls
        news_item["url"] = response.url
        news_item["image_url"] = response.xpath(
            "//meta[contains(@property, 'og:image')]/@content"
        ).get()

        # titles
        news_item["headline"] = (
            response.xpath("//meta[contains(@property, 'og:title')]/@content")
            .get()
            .partition(" | ")[0]
        )
        news_item["subtitle"] = cleanhtml_shorten(
            response.xpath("//p[contains(@style, 'text-align: justify')]/text()").get()
        )

        # date
        date_str = get_custom_dates(
            response.xpath(
                "//meta[contains(@property, 'article:modified_time')]/@content"
            ).get(),
            INVESTOPAPER,
        )
        news_item["date"] = date_str["eng"]
        news_item["nepdate"] = date_str["nep"]
        news_item["scraped_datetime"] = get_current_datetime_eng_custom()

        news_item["scrip"] = []

        yield news_item
