import scrapy
import json

from nepsescraper.items import MarketSummaryItem
from nepsescraper.utils.date_parsers import t_to_default


class MarketSummarySpider(scrapy.Spider):
    name = "market_summary"
    start_urls = ["https://newweb.nepalstock.com/api/nots/nepse-data/market-open"]

    def parse(self, response):
        raw_data = json.loads(response.text)
        updated_date = t_to_default(raw_data["asOf"])

        yield response.follow(
            "https://newweb.nepalstock.com/api/nots/market-summary/",
            callback=self.parse_detail,
            cb_kwargs=dict(updated_date=updated_date),
        )

    def parse_detail(self, response, updated_date):
        raw_data = json.loads(response.text)
        market_summary_item = MarketSummaryItem()

        market_summary_item["updated_date"] = updated_date
        market_summary_item["total_turnover"] = raw_data[0]["value"]
        market_summary_item["total_turnover"] = raw_data[0]["value"]
        market_summary_item["total_traded_shares"] = raw_data[1]["value"]
        market_summary_item["total_transactions"] = raw_data[2]["value"]
        market_summary_item["total_scrips_traded"] = raw_data[3]["value"]
        market_summary_item["total_market_cap"] = raw_data[4]["value"]
        market_summary_item["floated_market_cap"] = raw_data[5]["value"]

        yield market_summary_item
