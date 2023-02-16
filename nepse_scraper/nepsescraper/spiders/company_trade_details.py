import scrapy
import json

from humps import decamelize

from nepsescraper.items import CompanyTradeDetailItem


class CompanyTradeDetailSpider(scrapy.Spider):
    name = "company_trade_detail"
    start_urls = ["https://newweb.nepalstock.com/api/nots/company/list/"]

    def parse(self, response):
        raw_data = json.loads(response.body)

        ids = []
        for data in raw_data:
            if data["status"] == "A":
                ids.append(data["id"])

        for id in ids:
            yield response.follow(
                "https://newweb.nepalstock.com/api/nots/security/" + str(id),
                callback=self.parse_detail,
            )
        # yield response.follow(
        #     "https://newweb.nepalstock.com/api/nots/security/" + str(ids[0]),
        #     callback=self.parse_detail,
        # )

    def parse_detail(self, response):
        try:
            raw_data = json.loads(response.body)
            raw_security_detail = raw_data["securityDailyTradeDto"]

            trade_permission = lambda x: True if x == "Y" or x == "y" else False

            if trade_permission(raw_data["security"]["permittedToTrade"]):

                item = CompanyTradeDetailItem()

                item["security_symbol"] = raw_data["security"]["symbol"]
                item["security_name"] = raw_data["security"]["securityName"]

                for key, value in raw_security_detail.items():
                    item[decamelize(key)] = value

                yield item

            else:
                print("Not permitted to trade!")
                pass

        except KeyError as e:
            print(e)