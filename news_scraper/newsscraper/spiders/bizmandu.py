import re

import scrapy

from newsscraper.items import NewsItem
from newsscraper.utils.date_parsers import (
    get_current_datetime_eng_custom,
    get_custom_dates,
)
from newsscraper.utils.definitions import BIZMANDU, BIZMANDU_SEC


def cleanhtml(raw_html):
    cleanr = cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    cleantext = re.sub(cleanr, "", raw_html)
    cleantext = cleantext.replace("\n", "").replace("\t", "")
    return cleantext


class BizmanduSpider(scrapy.Spider):
    name = "bizmandu"
    allowed_domains = ["bizmandu.com"]
    start_urls = ["https://bizmandu.com/content/category/market.html"]

    def parse(self, response):
        news_item = NewsItem()

        # lead news
        lead_news = response.css("div.biz-cat-lead-news")
        if lead_news:
            news_item["source"] = "Bizmandu"
            # urls
            news_item["url"] = lead_news.css("a::attr(href)").get()
            img = lead_news.css("img.uk-thumbnail-expand")
            if img:
                news_item["image_url"] = (
                    "bizmandu.com/" + img.css("::attr(src)").get()[2:]
                )
            else:
                news_item["image_url"] = ""

            # titles
            news_item["headline"] = cleanhtml(lead_news.css("h2").get())
            news_item["subtitle"] = cleanhtml(
                lead_news.css("p:nth-child(4)").get()
                + lead_news.css("p:nth-child(5)").get()
            )

            # dates
            try:
                date_str = get_custom_dates(
                    lead_news.css("p.uk-article-meta::text").get().strip(), BIZMANDU
                )
            except:
                cleaned = cleanhtml(
                    lead_news.css("p.uk-article-meta::text")
                    .get()
                    .partition("बिजमाण्डू")[2]
                    .strip()
                )
                date_str = get_custom_dates(
                    cleaned,
                    BIZMANDU_SEC,
                )
            news_item["date"] = date_str["eng"]
            news_item["nepdate"] = date_str["nep"]
            news_item["scraped_datetime"] = get_current_datetime_eng_custom()

            yield news_item

        # Other news
        other_news = response.css(".biz-archive-panel li")
        for news in other_news:
            news_item["source"] = "Bizmandu"

            # urls
            news_item["url"] = news.css("a::attr(href)").get()
            img = news.css("img.uk-thumbnail-mini")
            if img:
                news_item["image_url"] = (
                    "bizmandu.com/"
                    + img.css("::attr(data-pagespeed-lazy-src)").get()[2:]
                )
            else:
                news_item["image_url"] = ""

            # titles
            news_item["headline"] = cleanhtml(news.css("h3").get())
            news_item["subtitle"] = cleanhtml(
                news.css("p:nth-child(4)").get() + news.css("p:nth-child(5)").get()
            )

            # dates
            try:
                cleaned = cleanhtml(
                    news.css("p.uk-article-meta::text")
                    .get()
                    .partition("बिजमाण्डू")[2]
                    .strip()
                )
                date_str = get_custom_dates(cleaned, BIZMANDU_SEC)
            except:
                date_str = get_custom_dates(
                    news.css("p.uk-article-meta::text").get(), BIZMANDU
                )
            news_item["date"] = date_str["eng"]
            news_item["nepdate"] = date_str["nep"]
            news_item["scraped_datetime"] = get_current_datetime_eng_custom()

            news_item["scrip"] = []

            yield news_item
