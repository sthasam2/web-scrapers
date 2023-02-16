import scrapy

from sebonscraper.items import RightSharePipelineItem, RightShareApprovedItem


class RightSharePipelineSpider(scrapy.Spider):
    name = "sebon_right_share_pipeline"
    start_urls = ["https://www.sebon.gov.np/right-share-pipeline"]
    page_number = 1

    def parse(self, response):
        item = RightSharePipelineItem()
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

        next_page = (
            RightSharePipelineSpider.start_urls[0]
            + "?page="
            + str(RightSharePipelineSpider.page_number)
        )

        if RightSharePipelineSpider.page_number <= max_page:
            RightSharePipelineSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class RightShareApprovedSpider(scrapy.Spider):
    name = "sebon_right_share_approved"
    start_urls = ["https://www.sebon.gov.np/right-share-approved"]
    page_number = 1

    def parse(self, response):
        item = RightShareApprovedItem()
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

        next_page = (
            RightShareApprovedSpider.start_urls[0]
            + "?page="
            + str(RightShareApprovedSpider.page_number)
        )

        if RightShareApprovedSpider.page_number <= max_page:
            RightShareApprovedSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)