import scrapy

from sebonscraper.items import BonusShareRegistrationItem


class BonusShareRegistrationSpider(scrapy.Spider):
    name = "sebon"
    start_urls = ["https://www.sebon.gov.np/bonus-share-segistered"]
    page_number = 1

    def parse(self, response):
        item = BonusShareRegistrationItem()
        rawdata = response.css("table.table tbody tr")
        max_page = (len(response.css("ul.pagination li.page-item ::text")) / 2) - 2

        for index in range(len(rawdata)):
            item["name"] = rawdata[index].xpath("td[1]//text()").extract()[0]
            item["date"] = rawdata[index].xpath("td[2]//text()").extract()[0]
            if len(rawdata[index].xpath("td[3]/a/@href").extract()) != 0:
                item["eng_pdf"] = rawdata[index].xpath("td[3]/a/@href").extract()[0]
            if len(rawdata[index].xpath("td[4]/a/@href").extract()) != 0:
                item["nep_pdf"] = rawdata[index].xpath("td[4]/a/@href").extract()[0]

            yield item

        next_page = "https://www.sebon.gov.np/bonus-share-segistered?page=" + str(
            BonusShareRegistrationSpider.page_number
        )

        if BonusShareRegistrationSpider.page_number <= max_page:
            BonusShareRegistrationSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def info(self, response):
        yield {
            "title": response.css("title::text").extract()[0],
            "header": response.css("h1::text").extract()[0],
        }