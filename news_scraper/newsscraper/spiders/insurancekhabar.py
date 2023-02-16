import scrapy

from newsscraper.items import NewsItem
from newsscraper.utils.cleaners import clean_insurancekhabar_date, cleanhtml_shorten
from newsscraper.utils.date_parsers import (
    get_current_datetime_eng_custom,
    get_custom_dates,
)
from newsscraper.utils.definitions import (
    CLEANED_INSURANCEKHABAR,
    INVESTOPAPER,
    UNICODE_CONVERTED_INSURANCEKHABAR,
)


class InsurancekhabarSpider(scrapy.Spider):
    name = "insurancekhabar"
    allowed_domains = ["insurancekhabar.com"]
    start_urls = ["http://insurancekhabar.com/category/news"]

    page_number = 1
    max_page = 1

    latest_news = None
    links = []

    def parse(self, response):
        page_links = response.css("article header a::attr(href)").extract()
        InsurancekhabarSpider.links += page_links

        if InsurancekhabarSpider.page_number < InsurancekhabarSpider.max_page:
            InsurancekhabarSpider.page_number += 1
            next_page = f"http://insurancekhabar.com/category/news/page/{InsurancekhabarSpider.page_number}"
            yield response.follow(next_page, callback=self.parse)

        # Executes news detail parsing after link collection is completed
        for link in InsurancekhabarSpider.links:
            yield response.follow(link, callback=self.news_detail_parse)

        InsurancekhabarSpider.latest_news = InsurancekhabarSpider.links[0]

    def news_detail_parse(self, response):
        """
        Get the detailed info from page
        """
        news_item = NewsItem()

        news_item["source"] = "InsuranceKhabar"

        # urls
        news_item["url"] = response.url
        news_item["image_url"] = response.xpath(
            "//meta[contains(@property, 'og:image')]/@content"
        ).get()

        # titles
        news_item["headline"] = response.xpath(
            "//meta[contains(@property, 'og:title')]/@content"
        ).get()
        news_item["subtitle"] = cleanhtml_shorten(
            response.xpath("//div[contains(@class, 'entry-content')]/p/text()").get()
        )

        # date
        cleaned = clean_insurancekhabar_date(response.css("span.posted-on::text").get())
        date_str = get_custom_dates(
            cleaned,
            CLEANED_INSURANCEKHABAR,
        )
        news_item["date"] = date_str["eng"]
        news_item["nepdate"] = date_str["nep"]
        news_item["scraped_datetime"] = get_current_datetime_eng_custom()

        yield news_item
