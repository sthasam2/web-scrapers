import scrapy

from ....utils.date_parsers import oldnepalstock_to_default
from oldnepsescraper.items import MarketSummaryItem


class NepalstockSpider(scrapy.Spider):
    name = "nepalstock"
    allowed_domains = ["nepalstock.com"]
    start_urls = ["http://nepalstock.com/"]

    def parse(self, response):
        summary_item = MarketSummaryItem()

        summary_item["updated_date"] = oldnepalstock_to_default(
            response.css("div#market-watch div.panel-heading::text").extract()[0]
        )

        for row in response.xpath(
            "/html/body/div[5]/div[2]/div[2]/div[2]/table/tbody/tr"
        ):
            summary_item["total_turnover"] = row[0].xpath("td[2]//text()").extract()[0]
            summary_item["total_traded_shares"] = (
                row[1].xpath("td[2]//text()").extract()[0]
            )
            summary_item["total_transactions"] = (
                row[2].xpath("td[2]//text()").extract()[0]
            )
            summary_item["total_scrips_traded"] = (
                row[3].xpath("td[2]//text()").extract()[0]
            )
            summary_item["total_market_cap"] = (
                row[4].xpath("td[2]//text()").extract()[0]
            )
            summary_item["floated_market_cap"] = (
                row[5].xpath("td[2]//text()").extract()[0]
            )

        yield summary_item