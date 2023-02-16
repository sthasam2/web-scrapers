import datetime as dt
import json

import scrapy

from newsscraper.items import NewsItem
from newsscraper.utils.cleaners import clean_merolagani_shorten
from newsscraper.utils.date_parsers import (
    get_current_datetime_eng_custom,
    get_custom_dates,
)
from newsscraper.utils.definitions import MEROLAGANI, MEROLAGANI_SHORT


class MerolaganiSpider(scrapy.Spider):
    name = "merolagani"
    allowed_domains = ["merolagani.com"]
    start_urls = [
        "https://merolagani.com/handlers/webrequesthandler.ashx?type=get_news&newsID=0&newsCategoryID=0&symbol=&page=1&pageSize=40&popular=false&includeFeatured=true&news=%23ctl00_ContentPlaceHolder1_txtNews&languageType=NP"
    ]

    def parse(self, response):
        news_item = NewsItem()

        raw_data = json.loads(response.text)
        for data in raw_data:
            news_item["source"] = "Merolagani"

            # urls
            news_item["url"] = "https://merolagani.com/NewsDetail.aspx?newsID=" + str(
                data["newsID"]
            )
            news_item["image_url"] = (
                "https://images.merolagani.com/Uploads/Repository/"
                + data["imagePath"].partition("\\")[2]
            )

            # titles
            news_item["headline"] = data["newsTitle"]
            news_item["subtitle"] = clean_merolagani_shorten(data["newsOverview"])

            # dates
            try:
                date_str = get_custom_dates(data["newsDateAD"], MEROLAGANI)
            except:
                date_str = get_custom_dates(
                    data["newsDateAD"],
                    MEROLAGANI_SHORT,
                )
            news_item["date"] = date_str["eng"]
            news_item["nepdate"] = date_str["nep"]
            news_item["scraped_datetime"] = get_current_datetime_eng_custom()
            news_item["scrip"] = []

            yield news_item
