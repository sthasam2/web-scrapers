import scrapy
import json

from humps import decamelize

from nepsescraper.items import CompanyPriceDetailItem


class CompanyPriceHistorySpider(scrapy.Spider):
    name = "company_price_history"
    start_urls = ["https://newweb.nepalstock.com/api/nots/company/list/"]

    def parse(self, response):
        raw_data = json.loads(response.body)

        ids = []
        for data in raw_data:
            if data["status"] == "A":
                ids.append(data["id"])

        for id in ids:
            yield response.follow(
                f"https://newweb.nepalstock.com/api/nots/market/security/price/{str(id)}?size=100",
                callback=self.parse_detail,
            )
        # yield response.follow(
        #     f"https://newweb.nepalstock.com/api/nots/market/security/price/{str(ids[0])}?size=100",
        #     callback=self.parse_detail,
        # )

    def parse_detail(self, response):
        try:
            raw_data = json.loads(response.body)
            raw_content = raw_data["content"]

            item = CompanyPriceDetailItem()

            for content in raw_content:
                item["security_symbol"] = content["security"]["symbol"]
                item["security_name"] = content["security"]["securityName"]
                item["security_id"] = content["security"]["id"]

                for key, value in content.items():

                    if key != "security":
                        item[decamelize(key)] = value

                yield item

        except KeyError as e:
            print(e)