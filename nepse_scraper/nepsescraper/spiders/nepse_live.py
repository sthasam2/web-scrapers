import scrapy
import json

from nepsescraper.items import LiveMarketItem


class LiveMarketSpider(scrapy.Spider):
    name = "nepse_live"
    start_urls = ["https://newweb.nepalstock.com/api/nots/live-market"]
    status = "CLOSED"

    def parse(self, response):
        raw_data = json.loads(response.text)
        live_market_item = LiveMarketItem()

        for data in raw_data:
            live_market_item["security_id"] = data["securityId"]
            live_market_item["symbol"] = data["symbol"]
            live_market_item["company"] = data["securityName"]
            live_market_item["ltp"] = data["lastTradedPrice"]
            live_market_item["ltv"] = data["lastTradedVolume"]
            live_market_item["point_change"] = (
                data["lastTradedPrice"] - data["previousClose"]
            )
            live_market_item["perc_change"] = data["percentageChange"]
            live_market_item["open_price"] = data["openPrice"]
            live_market_item["high_price"] = data["highPrice"]
            live_market_item["low_price"] = data["lowPrice"]
            live_market_item["volume"] = data["totalTradeQuantity"]
            live_market_item["prev_closing"] = data["previousClose"]

            yield live_market_item