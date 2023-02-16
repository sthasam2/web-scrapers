import scrapy

from newsscraper.items import NewsItem
from newsscraper.utils.date_parsers import (
    get_current_datetime_eng_custom,
    get_custom_dates,
)
from newsscraper.utils.definitions import SHARESANSAR


# class SharesansarSpider(scrapy.Spider):
#     name = "sharesansar"
#     allowed_domains = ["sharesansar.com"]
#     start_urls = ["http://sharesansar.com/category/latest"]
#     page_number = 1
#     max_page = 3

#     def parse(self, response):
#         news_item = SharesansarItem()

#         for index in range(
#             1, len(response.css("div.featured-news-list").extract()) + 1
#         ):
#             news_item["url"] = response.css(
#                 "div.featured-news-list:nth-child(" + str(index) + ") a::attr(href)"
#             ).extract()[0]

#             news_item["image_url"] = response.css(
#                 "div.featured-news-list:nth-child(" + str(index) + ") img::attr(src)"
#             ).extract()[0]

#             news_item["headline"] = response.css(
#                 "div.featured-news-list:nth-child("
#                 + str(index)
#                 + ") h4.featured-news-title::text"
#             ).extract()[0]

#             news_item["date"] = response.css(
#                 "div.featured-news-list:nth-child("
#                 + str(index)
#                 + ") span.text-org::text"
#             ).extract()[0]
#             news_item["scraped_datetime"] = get_current_datetime_eng_custom()

#             yield news_item

#         if SharesansarSpider.page_number < SharesansarSpider.max_page:
#             SharesansarSpider.page_number += 1
#             next_page = f"https://www.sharesansar.com/category/latest?page={SharesansarSpider.page_number}"
#             yield response.follow(next_page, callback=self.parse)


class SharesansarSpider(scrapy.Spider):
    name = "sharesansar"
    allowed_domains = ["sharesansar.com"]
    start_urls = ["http://sharesansar.com/category/latest"]

    page_number = 1
    max_page = 3

    last_news = None
    links = []

    def parse(self, response):
        # links
        page_links = response.css(
            ".featured-news-list div:nth-child(1) a::attr(href)"
        ).extract()
        SharesansarSpider.links += page_links

        if SharesansarSpider.page_number < SharesansarSpider.max_page:
            SharesansarSpider.page_number += 1
            next_page = f"https://www.sharesansar.com/category/latest?page={SharesansarSpider.page_number}"
            yield response.follow(next_page, callback=self.parse)

        # Executes news detail parsing after link collection is completed
        for link in SharesansarSpider.links:
            yield response.follow(link, callback=self.news_detail_parse)

        SharesansarSpider.latest_news = SharesansarSpider.links[0]

    def news_detail_parse(self, response):
        """
        Get the detailed info from page
        """
        news_item = NewsItem()

        news_item["source"] = "ShareSansar"

        # urls
        news_item["url"] = response.url
        news_item["image_url"] = response.xpath(
            "//meta[contains(@property, 'og:image')]/@content"
        ).get()

        # titles
        news_item["headline"] = response.xpath(
            "//meta[contains(@property, 'og:title')]/@content"
        ).get()
        news_item["subtitle"] = (
            response.xpath("//meta[contains(@property, 'og:description')]/@content")
            .get()
            .partition(" || ")[2]
        )

        # date
        date_str = get_custom_dates(
            response.css("div.col-lg-8 h5::text").get().strip().partition("\n")[0],
            SHARESANSAR,
        )
        news_item["date"] = date_str["eng"]
        news_item["nepdate"] = date_str["nep"]
        news_item["scraped_datetime"] = get_current_datetime_eng_custom()

        news_item["scrip"] = []

        yield news_item


# FIXME REFACTOR FOR EACH LINK