import scrapy
import json

from nepsescraper.items import FloorsheetItem


class NepseSpider(scrapy.Spider):
    name = "nepse"
    allowed_domains = ["newweb.nepalstock.com"]
    start_urls = [
        "https://newweb.nepalstock.com/api/nots/nepse-data/floorsheet?page=0&size=500&sort=contractId,desc"
    ]

    floorsheet_item = FloorsheetItem()

    def parse(self, response):
        raw_data = json.loads(response.text)
        max_page = raw_data["floorsheets"]["totalPages"]
        page_number = 0

        while page_number <= max_page:
            next_page = f"https://newweb.nepalstock.com/api/nots/nepse-data/floorsheet?page={page_number}&size=500&sort=contractId,desc"
            yield response.follow(next_page, callback=self.parse_floorsheet_items)
            page_number += 1

    def parse_floorsheet_items(self, response):
        raw_data = json.loads(response.text)
        item = self.floorsheet_item
        # floorsheets = raw_data["floorsheets"]["content"]
        for floorsheet in raw_data["floorsheets"]["content"]:
            item["contract_id"] = floorsheet["contractId"]
            item["stock_symbol"] = floorsheet["stockSymbol"]
            item["buyer_member_id"] = floorsheet["buyerMemberId"]
            item["seller_member_id"] = floorsheet["sellerMemberId"]
            item["contract_quantity"] = floorsheet["contractQuantity"]
            item["contract_rate"] = floorsheet["contractRate"]
            item["contract_amount"] = floorsheet["contractAmount"]
            item["business_date"] = floorsheet["businessDate"]
            item["trade_book_id"] = floorsheet["tradeBookId"]
            item["stock_id"] = floorsheet["stockId"]
            item["buyer_broker_name"] = floorsheet["buyerBrokerName"]
            item["seller_broker_name"] = floorsheet["sellerBrokerName"]
            item["security_name"] = floorsheet["securityName"]

            yield item